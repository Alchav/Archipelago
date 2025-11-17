local productivity_overlay_icon = {
  icon = "__core__/graphics/icons/technology/effect-constant/effect-constant-recipe-productivity.png",
  icon_size = 64
}

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
    for level = 1, 30 do
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
            change = 0.1
          }
        },
        prerequisites = prerequisites,
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
            prerequisites = {"mining-productivity-2", "production-science-pack", "utility-science-pack"},
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
            prerequisites = {"follower-robot-count-4", "space-science-pack"},
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
            prerequisites = {"worker-robots-speed-5", "space-science-pack"},
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
            prerequisites = {"physical-projectile-damage-6", "space-science-pack"},
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
            prerequisites = {"stronger-explosives-6", "space-science-pack"},
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
            prerequisites = {"refined-flammables-6", "space-science-pack"},
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
            prerequisites = {"laser-weapons-damage-6", "space-science-pack"},
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
        prerequisites = {"artillery", "space-science-pack"},
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
        prerequisites = {"artillery", "space-science-pack"},
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