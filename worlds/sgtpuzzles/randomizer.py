from random import Random

class PuzzleRandomizer:
    def __init__(
            self,
            builtin_presets: dict[str, list[tuple[str, int, int]]],
            preset_overrides: dict[str, list[str]|dict[str, int]],
            random: Random,
            entries: list = None,
            weights: list[float|int] = None,
            selfweight: float|int = 1,
            mode: str = "default",
            count: int = None,
            min_count: int = None,
            max_count: int = None,
            min_difficulty: int = 0,
            max_difficulty: int = 2,
            genre_min_difficulty: dict[str, int] = None,
            genre_max_difficulty: dict[str, int] = None,
            ):
        self.entries: list[str|PuzzleRandomizer] = entries if entries is not None else []
        self.weights: list[float|int] = weights if weights is not None else [(elem.selfweight if elem is PuzzleRandomizer else 1) for elem in self.entries]
        self.selfweight: float|int = selfweight

        # Valid options are "default", "bag", "exact"
        self.mode: str = mode

        self.max_count: int = max_count if max_count is not None else (count if count is not None else (len(self.entries) if self.mode == "exact" else 1))
        self.min_count: int = min_count if min_count is not None else self.max_count

        self.min_difficulty: int = min_difficulty
        self.max_difficulty: int = max_difficulty
        self.genre_min_difficulty: dict[str, int] = genre_min_difficulty if genre_min_difficulty is not None else {}
        self.genre_max_difficulty: dict[str, int] = genre_max_difficulty if genre_max_difficulty is not None else {}

        self.builtin_presets: dict[str,list[tuple[str, int, int]]] = builtin_presets
        self.preset_overrides: dict[str,list[str]|dict[str,int]] = preset_overrides
        self.random: Random = random

    def evaluate(self) -> list[str]:
        usable_presets = self._get_usable_presets()

        is_invalid_entry = [isinstance(entry, str) and ("#" not in entry) and (len(usable_presets[entry][0]) == 0) for entry in self.entries]

        entries = [self.entries[i] for i in range(len(self.entries)) if not is_invalid_entry[i]]
        weights = [self.weights[i] for i in range(len(self.weights)) if not is_invalid_entry[i]]

        components = []

        count = self.random.randint(self.min_count, self.max_count)

        if self.mode == "default":
            components = self.random.choices(entries, k=count, weights=weights)

            if count > 0 and len(self.entries) == 0:
                raise ValueError("No valid entries to randomize.")
        elif self.mode == "bag":
            components = self.random.sample(entries, k=count, counts=weights)

            if count > len(self.entries):
                raise ValueError("Not enough valid entries to randomize.")
        elif self.mode == "exact":
            components = self.entries # TODO: duplicate by weights?

        result: list[str] = []

        for entry in components:
            if isinstance(entry, str):
                newPuzzle = self._get_random_preset(entry, usable_presets)
                if result is not None:
                    result.append(newPuzzle)
            elif isinstance(entry, PuzzleRandomizer):
                newPuzzles = entry.evaluate()
                result = result + newPuzzles

        return result
    
    def _get_usable_presets(self):
        result = {}

        for genre in self.builtin_presets:
            if genre in self.preset_overrides:
                genreEntries = self.preset_overrides[genre]
                if isinstance(genreEntries, list):
                    result[genre] = (genreEntries, [1 for _ in genreEntries])
                elif isinstance(genreEntries, dict):
                    result[genre] = (list(genreEntries.keys()), list(genreEntries.values()))
            else:
                genre_presets = self.builtin_presets[genre]
                max_difficulty = self.max_difficulty
                min_difficulty = self.min_difficulty

                if genre in self.genre_min_difficulty:
                    min_difficulty = self.genre_min_difficulty[genre]
                    max_difficulty = max(min_difficulty, max_difficulty)

                if genre in self.genre_max_difficulty:
                    max_difficulty = self.genre_max_difficulty[genre]
                    min_difficulty = min(min_difficulty, max_difficulty)

                is_valid = [min_difficulty <= entry[2] <= max_difficulty for entry in genre_presets]
                entries = [genre_presets[i][0] for i in range(len(genre_presets)) if is_valid[i]]
                weights = [genre_presets[i][1] for i in range(len(genre_presets)) if is_valid[i]]

                result[genre] = (entries, weights)

        return result

    def _get_random_preset(self, spec: str, usable_presets):
        if "#" in spec:
            return spec

        genre_presets = usable_presets[spec]
        if len(genre_presets[0]) == 0:
            # This should never happen
            return None

        parameters = self.random.choices(genre_presets[0], k=1, weights=genre_presets[1])[0]
        return f"{spec}:{parameters}"