-- data-final-fixes.lua
local util = require("util")

local technologies = data.raw.technology
local recipes = data.raw.recipe

local techs_to_delete = {}
local dont_delete = {}  -- <--- NEW

-- === Helpers ===============================================================

-- Find any prototype with this name that has an icon/icons
local function find_prototype_with_icon(name)
  if not name then return nil end
  for _, proto_group in pairs(data.raw) do
    local proto = proto_group[name]
    if proto and (proto.icon or proto.icons) then
      return proto
    end
  end
  return nil
end

-- Copy icon/icons/icon_size/icon_mipmaps from src to dest
local function copy_icon_from_prototype(dest, src)
  if src.icons then
    dest.icons = util.table.deepcopy(src.icons)
    dest.icon = nil
    dest.icon_size = nil
    dest.icon_mipmaps = nil
  else
    dest.icons = nil
    dest.icon = src.icon
    dest.icon_size = src.icon_size
    dest.icon_mipmaps = src.icon_mipmaps
  end
end

-- Choose an icon for the new tech from recipe or its main product
local function assign_icon_from_recipe_or_product(new_tech, recipe, fallback_icon_proto, tech_name)
  -- 1) Recipe has its own icon/icons
  if recipe.icons or recipe.icon then
    copy_icon_from_prototype(new_tech, recipe)
    return
  end

  -- 2) Try main product / results / result
  local product_name = nil

  if recipe.main_product then
    if type(recipe.main_product) == "string" then
      product_name = recipe.main_product
    elseif type(recipe.main_product) == "table" and recipe.main_product.name then
      product_name = recipe.main_product.name
    end
  end

  if not product_name and recipe.result then
    product_name = recipe.result
  end

  if not product_name and recipe.results and #recipe.results > 0 then
    local first = recipe.results[1]
    if type(first) == "table" then
      product_name = first.name or first[1]
    else
      -- results can also be {"item-name", amount}
      product_name = first
    end
  end

  if product_name then
    local product_proto = find_prototype_with_icon(product_name)
    if product_proto then
      copy_icon_from_prototype(new_tech, product_proto)
      return
    else
      log("Could not find prototype with icon for product '" ..
          tostring(product_name) .. "' from recipe '" ..
          tostring(recipe.name) .. "' (tech '" .. tostring(tech_name) .. "').")
    end
  else
    log("No product_name found for recipe '" ..
        tostring(recipe.name) .. "' (tech '" .. tostring(tech_name) .. "').")
  end

  -- 3) Fallback: keep the original tech icon so we don't break the prototype
  if fallback_icon_proto then
    copy_icon_from_prototype(new_tech, fallback_icon_proto)
  else
    log("No icon available for new tech from recipe '" ..
        tostring(recipe.name) .. "' (tech '" .. tostring(tech_name) .. "').")
  end
end

-- Set of recipes that should also unlock circuit network
local circuit_network_recipes = {
  ["arithmetic-combinator"]   = true,
  ["decider-combinator"]      = true,
  ["constant-combinator"]     = true,
  ["power-switch"]            = true,
  ["programmable-speaker"]    = true,
  ["display-panel"]           = true,
}

-- Add special effects based on recipe name
local function apply_special_effects(new_tech, recipe_name)
  -- construction-robot: {type = "create-ghost-on-entity-death", modifier = true}
  if recipe_name == "construction-robot" then
    table.insert(new_tech.effects, {
      type = "create-ghost-on-entity-death",
      modifier = true
    })
  end

  -- rail-ramp : {type = "rail-planner-allow-elevated-rails", modifier = true}
  if recipe_name == "rail-ramp" then
    table.insert(new_tech.effects, {
        type = "rail-planner-allow-elevated-rails",
        modifier = true
    })
  end

  -- logistic-robot:
  -- {type = "character-logistic-requests", modifier = true}
  -- {type = "character-logistic-trash-slots", modifier = 30}
  if recipe_name == "logistic-robot" then
    table.insert(new_tech.effects, {
      type = "character-logistic-requests",
      modifier = true
    })
    table.insert(new_tech.effects, {
      type = "character-logistic-trash-slots",
      modifier = 30
    })
  end

  -- requester-chest: {type = "vehicle-logistics", modifier = true}
  if recipe_name == "requester-chest" then
    table.insert(new_tech.effects, {
      type = "vehicle-logistics",
      modifier = true
    })
  end

  -- circuit network unlock
  if circuit_network_recipes[recipe_name] then
    -- avoid duplicate unlock-circuit-network if already present for some reason
    local already = false
    for _, eff in ipairs(new_tech.effects) do
      if eff.type == "unlock-circuit-network" then
        already = true
        break
      end
    end
    if not already then
      table.insert(new_tech.effects, {
        type = "unlock-circuit-network",
        modifier = true
      })
    end
  end
end

-- === Main tech splitting pass ==============================================

for tech_name, tech in pairs(technologies) do
  local effects = tech.effects
  local unlock_effects = {}
  local has_other_effects = false

  if effects then
    for _, effect in pairs(effects) do
      if effect.type == "unlock-recipe" then
        table.insert(unlock_effects, effect)
      else
        has_other_effects = true
      end
    end
  end

  local unlock_count = #unlock_effects

  if tech_name == "rocket-silo" then
    tech.effects = {{type = "unlock-recipe", recipe = "rocket-silo"},{type = "unlock-recipe", recipe = "rocket-part"}}
    -- Never delete rocket-silo in the cleanup pass
    dont_delete["rocket-silo"] = true
  end
  if unlock_count < 2 then
    -- Case 1: 0 or 1 unlock-recipe effect → just remove prerequisites

    tech.prerequisites = nil

  elseif unlock_count >= 2 then
    -- Case 2: multiple unlock-recipe effects (excluding rocket-part on rocket-silo)
    if has_other_effects then
      log("Tech '" .. tech_name ..
          "' has multiple unlock-recipe effects AND other effects; needs special handling.")
    end

    -- NEW: detect if this tech has a recipe with the same name as the tech
    local tech_name_matches_recipe = false
    for _, unlock in ipairs(unlock_effects) do
      if unlock.recipe == tech_name then
        tech_name_matches_recipe = true
        break
      end
    end
    if tech_name_matches_recipe then
      dont_delete[tech_name] = true
    end

    -- Capture original icon as a fallback if recipe/item lookup fails
    local original_icon_proto = {
      icon = tech.icon,
      icons = tech.icons,
      icon_size = tech.icon_size,
      icon_mipmaps = tech.icon_mipmaps
    }

    local base = util.table.deepcopy(tech)
    base.effects = nil
    base.prerequisites = nil

    for _, unlock in ipairs(unlock_effects) do
      local recipe_name = unlock.recipe
      if recipe_name ~= "rocket-part" then
          local recipe = recipes[recipe_name]

          if not recipe then
            log("Recipe '" .. tostring(recipe_name) ..
                "' from tech '" .. tech_name .. "' not found; skipping.")
          else
            local new = util.table.deepcopy(base)

            new.name = recipe_name
            new.localised_name =
              {recipe_name}

            assign_icon_from_recipe_or_product(new, recipe, original_icon_proto, tech_name)

            new.effects = {
              {
                type = "unlock-recipe",
                recipe = recipe_name
              }
            }

            apply_special_effects(new, recipe_name)
            new.prerequisites = nil

            data:extend({ new })
          end
      end
    end

    table.insert(techs_to_delete, tech_name)
  else
    tech.prerequisites = nil
  end
end

-- === Remove original multi-unlock techs ====================================

for _, tech_name in ipairs(techs_to_delete) do
  if not dont_delete[tech_name] then  -- <--- NEW CHECK
    if tech_name == "circuit-network" then
      data.raw.technology[tech_name].effects = {
        {type = "unlock-circuit-network", modifier = true}
      }
      data.raw.technology[tech_name].prerequisites = {}
    else
      data.raw.technology[tech_name] = nil
    end
  end
end

-- Clean up prerequisites that point at deleted techs
local removed_lookup = {}
for _, name in ipairs(techs_to_delete) do
  if not dont_delete[name] then      -- <--- NEW CHECK
    removed_lookup[name] = true
  end
end

for _, tech in pairs(data.raw.technology) do
  if tech.prerequisites then
    local new_prereqs = {}
    for _, pre in ipairs(tech.prerequisites) do
      if not removed_lookup[pre] then
        table.insert(new_prereqs, pre)
      end
    end
    if #new_prereqs == 0 then
      tech.prerequisites = nil
    else
      tech.prerequisites = new_prereqs
    end
  end
end

-- === Shortcut fixups =======================================================

if data.raw.shortcut then
  for _, shortcut in pairs(data.raw.shortcut) do
    local tech = shortcut.technology_to_unlock
    if tech == "construction-robotics" then
      shortcut.technology_to_unlock = "construction-robot"
    elseif tech == "electronics" then
      shortcut.technology_to_unlock = "copper-cable"
    elseif tech == "artillery" then
      shortcut.technology_to_unlock = "artillery-shell"
    end
  end
end

data.raw["tips-and-tricks-item"] = {}
data.raw["research-achievement"]["eco-unfriendly"].technology = "basic-oil-processing"

data.raw.technology["rocket-silo"].effects = {{type = "unlock-recipe", recipe = "rocket-silo"},{type = "unlock-recipe", recipe = "rocket-part"}}

local productivity_overlay_icon = {
  icon = "__core__/graphics/icons/technology/effect-constant/effect-constant-recipe-productivity.png",
  icon_size = 64
}
local hide = true
local technologies = {}
local enabled_or_tech_recipes = {}

----------------------------------------------------------------
-- Enabled or unlocked recipes
----------------------------------------------------------------

local function is_enabled_by_default(recipe)
  -- In 2.0, nil == enabled
  return recipe.enabled ~= false
end

-- PASS 1: recipes enabled by default
for name, recipe in pairs(data.raw.recipe) do
  if is_enabled_by_default(recipe) then
    enabled_or_tech_recipes[name] = true
  end
end

-- PASS 2: recipes unlocked by technologies
for _, tech in pairs(data.raw.technology) do
  if tech.effects then
    for _, effect in pairs(tech.effects) do
      if effect.type == "unlock-recipe"
        and effect.recipe
        and data.raw.recipe[effect.recipe] then
        enabled_or_tech_recipes[effect.recipe] = true
      end
    end
  end
end

----------------------------------------------------------------
-- Helpers for results and icons
----------------------------------------------------------------

local function get_results_table(recipe)
  if recipe.results then
    return recipe.results
  end

  if recipe.result then
    return {{
      type   = recipe.result_type or "item",
      name   = recipe.result,
      amount = recipe.result_count or 1
    }}
  end

  return nil
end

local function icons_from_proto_name(name)
  if not name then return nil end

  local proto
  local item_types = {
    "item", "fluid", "ammo", "capsule", "gun", "armor", "tool",
    "module", "rail-planner", "item-with-entity-data",
    "item-with-label", "item-with-inventory", "item-with-tags"
  }

  for _, t in ipairs(item_types) do
    if data.raw[t] and data.raw[t][name] then
      proto = data.raw[t][name]
      break
    end
  end

  if not proto then return nil end

  if proto.icons then
    return table.deepcopy(proto.icons)
  elseif proto.icon then
    return {{
      icon = proto.icon,
      icon_size = proto.icon_size or 64,
      icon_mipmaps = proto.icon_mipmaps
    }}
  end

  return nil
end

local function get_recipe_icons(recipe)
  -- 1) icons on the recipe itself
  if recipe.icons then
    return table.deepcopy(recipe.icons)
  end
  if recipe.icon then
    return {{
      icon = recipe.icon,
      icon_size = recipe.icon_size or 64,
      icon_mipmaps = recipe.icon_mipmaps
    }}
  end

  -- 2) main_product
  if recipe.main_product then
    local icons = icons_from_proto_name(recipe.main_product)
    if icons then return icons end
  end

  -- 3) exactly one result -> use that prototype’s icon
  local results = get_results_table(recipe)
  if results and #results == 1 then
    local r = results[1]
    local name = r.name or r[1]
    local icons = icons_from_proto_name(name)
    if icons then return icons end
  end

  -- Nothing usable
  return nil
end

----------------------------------------------------------------
-- Generate technologies
----------------------------------------------------------------
all_recipes = {}
for recipe_name, recipe in pairs(data.raw.recipe) do
  local process = true

  if string.find(recipe_name, "parameter", 1, true) then
    process = false
  end

  -- Must be enabled by default or unlocked by tech
  if enabled_or_tech_recipes[recipe_name] ~= true then
    process = false
  end

  -- Skip hidden / factoriopedia-hidden recipes
  if recipe.hidden or recipe.hidden_in_factoriopedia then
    process = false
  end

  -- Skip recipes where *all* results are ignored_by_stats
  local results = get_results_table(recipe)
  if process then
    local skip_all_ignored = true

    if results then
      for _, result in ipairs(results) do
        if result.ignored_by_stats ~= result.amount then
          skip_all_ignored = false
          break
        end
      end
    else
      -- no results at all => don't treat as "all ignored"
      skip_all_ignored = false
    end

    if skip_all_ignored then
      process = false
    end
  end


  -- Resolve base recipe icons (recipe/main_product/single result)
  local base_icons = nil
  if process then
    base_icons = get_recipe_icons(recipe)
    if not base_icons then
      process = false
    end
  end

  if process then
    all_recipes[#all_recipes + 1] = recipe_name
    for level = 1, 3 do
      local tech_name = recipe_name .. "-productivity-" .. level

      local icons = table.deepcopy(base_icons)
      icons[#icons + 1] = table.deepcopy(productivity_overlay_icon)

      local count = math.floor(1000 * (1.5 ^ (level - 1)))

      local prerequisites = {}
      if level > 1 then
        prerequisites[1] = recipe_name .. "-productivity-" .. (level - 1)
      end

      local tech = {
        type = "technology",
        name = tech_name,
        icons = icons,
        effects = {
          {
            type = "change-recipe-productivity",
            recipe = recipe_name,
            change = 0.5
          }
        },
        prerequisites = prerequisites,
        hidden = hide,
        hidden_in_factoriopedia = hide,
        unit = {
          count = count,
          ingredients = {
            {"automation-science-pack", 1}
            -- add more packs here if you want
          },
          time = 60
        },
        upgrade = true,
        order = "z[prod-" .. recipe_name .. "-productivity]-" .. string.format("%02d", level),
      }

      technologies[#technologies + 1] = tech
    end
  end
end
data:extend(technologies)
universal_effects = {}
for i, recipe_name in ipairs(all_recipes) do
    table.insert(universal_effects, {type = "change-recipe-productivity", recipe = recipe_name, change = 0.01})
end

for level = 1, 150 do
   data.raw.technology["universal-productivity-" .. level] = {
        type = "technology",
        name = "universal-productivity-" .. level,
        icons = {productivity_overlay_icon},
        effects = universal_effects,
        prerequisites = prerequisites,
        hidden = hide,
        hidden_in_factoriopedia = hide,
        unit = {
          count = 1000,
          ingredients = {
            {"automation-science-pack", 1}
            -- add more packs here if you want
          },
          time = 60
        },
        upgrade = true,
        order = "z[universal-productivity-" .. level .. "]-" .. string.format("%02d", level),
   }
end
for level = 1, 30 do
    data.raw.technology["beacon-distribution-" .. level] = {
        type = "technology",
        name = "beacon-distribution-" .. level,
        icons = util.technology_icon_constant_movement_speed("__base__/graphics/technology/effect-transmission.png"),
--         infer_icon = false,
        effects = {{type = "beacon-distribution", modifier = 0.1}},
        upgrade = true,
        unit = {
            count = 1,
            time = 60,
            ingredients = {
                {"automation-science-pack", 1}
            }
        }
    }
    data.raw.technology["research-productivity-" .. level] = {
        type = "technology",
        name = "research-productivity-" .. level,
        icons = util.technology_icon_constant_productivity("__base__/graphics/technology/research-speed.png"),
--         infer_icon = false,
        effects =     {
            {
            type = "laboratory-productivity",
            modifier = 0.10
          },
        },
        upgrade = true,
        unit = {
            count = 1,
            time = 60,
            ingredients = {
                {"automation-science-pack", 1}
            }
        }
    }
    if level > 3 then
        data.raw.technology["mining-productivity-" .. level] = {
            type = "technology",
            name = "mining-productivity-" .. level,
            icons = util.technology_icon_constant_productivity("__base__/graphics/technology/mining-productivity.png"),
            effects =
            {
              {
                type = "mining-drill-productivity-bonus",
                modifier = 0.1
              }
            },
--             prerequisites = {"mining-productivity-2", "production-science-pack", "utility-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
    end
    if level > 4 then
        data.raw.technology["follower-robot-count-" .. level] =  {
            type = "technology",
            name = "follower-robot-count-" .. level,
            icons = util.technology_icon_constant_followers("__base__/graphics/technology/follower-robots.png"),
            effects =
            {
              {
                type = "maximum-following-robots-count",
                modifier = 25
              }
            },
--             prerequisites = {"follower-robot-count-4", "space-science-pack"},
            unit =
            {
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 30,
              count = 1000,
            },
            upgrade = true
        }
    end
    if level > 5 then
        data.raw.technology["worker-robots-speed-" .. level] =   {
            type = "technology",
            name = "worker-robots-speed-" ..level,
            icons = util.technology_icon_constant_movement_speed("__base__/graphics/technology/worker-robots-speed.png"),
            effects =
            {
              {
                type = "worker-robot-speed",
                modifier = 0.65
              }
            },
--             prerequisites = {"worker-robots-speed-5", "space-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
    end
    if level > 6 then
        data.raw.technology["physical-projectile-damage-" .. level] =     {
            type = "technology",
            name = "physical-projectile-damage-" .. level,
            icons = util.technology_icon_constant_damage("__base__/graphics/technology/physical-projectile-damage-2.png"),
            effects =
            {
              {
                type = "ammo-damage",
                ammo_category = "bullet",
                modifier = 0.4
              },
              {
                type = "turret-attack",
                turret_id = "gun-turret",
                modifier = 0.7
              },
              {
                type = "ammo-damage",
                ammo_category = "shotgun-shell",
                modifier = 0.4
              },
              {
                type = "ammo-damage",
                ammo_category = "cannon-shell",
                modifier = 1
              }
            },
--             prerequisites = {"physical-projectile-damage-6", "space-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
        data.raw.technology["stronger-explosives-" .. level] =   {
            type = "technology",
            name = "stronger-explosives-" .. level,
            icons = util.technology_icon_constant_damage("__base__/graphics/technology/stronger-explosives-3.png"),
            effects =
            {
              {
                type = "ammo-damage",
                ammo_category = "rocket",
                modifier = 0.5
              },
              {
                type = "ammo-damage",
                ammo_category = "grenade",
                modifier = 0.2
              },
              {
                type = "ammo-damage",
                ammo_category = "landmine",
                modifier = 0.2
              }
            },
--             prerequisites = {"stronger-explosives-6", "space-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
        data.raw.technology["refined-flammables-" .. level] =   {
            type = "technology",
            name = "refined-flammables-" .. level,
            icons = util.technology_icon_constant_damage("__base__/graphics/technology/refined-flammables.png"),
            effects =
            {
              {
                type = "ammo-damage",
                ammo_category = "flamethrower",
                modifier = 0.2
              },
              {
                type = "turret-attack",
                turret_id = "flamethrower-turret",
                modifier = 0.2
              }
            },
--             prerequisites = {"refined-flammables-6", "space-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
        data.raw.technology["laser-weapons-damage-" .. level] =   {
            type = "technology",
            name = "laser-weapons-damage-" .. level,
            icons = util.technology_icon_constant_damage("__base__/graphics/technology/laser-weapons-damage.png"),
            effects =
            {
              {
                type = "ammo-damage",
                ammo_category = "laser",
                modifier = 0.7
              },
              {
                type = "ammo-damage",
                ammo_category = "electric",
                modifier = 0.7
              },
              {
                type = "ammo-damage",
                ammo_category = "beam",
                modifier = 0.3
              }
            },
--             prerequisites = {"laser-weapons-damage-6", "space-science-pack"},
            unit =
            {
              count = 1000,
              ingredients =
              {
                {"automation-science-pack", 1}
              },
              time = 60
            },
            upgrade = true
        }
    end
    data.raw.technology["artillery-shell-range-" .. level] =   {
        type = "technology",
        name = "artillery-shell-range-" .. level,
        icons = util.technology_icon_constant_range("__base__/graphics/technology/artillery-range.png"),
        effects =
        {
          {
            type = "artillery-range",
            modifier = 0.3
          }
        },
--         prerequisites = {"space-science-pack"},
        unit =
        {
          count = 1000,
          ingredients =
          {
            {"automation-science-pack", 1}
          },
          time = 60
        },
        upgrade = true
    }
    data.raw.technology["artillery-shell-speed-" .. level] = {
        type = "technology",
        name = "artillery-shell-speed-" .. level,
        icons = util.technology_icon_constant_speed("__base__/graphics/technology/artillery-speed.png"),
        effects =
        {
          {
            type = "gun-speed",
            ammo_category = "artillery-shell",
            icon = "__base__/graphics/icons/artillery-shell.png",
            modifier = 1
          }
        },
--         prerequisites = {"space-science-pack"},
        unit =
        {
          count = 1000,
          ingredients =
          {
            {"automation-science-pack", 1},
          },
          time = 60
        },
        upgrade = true
    }
end