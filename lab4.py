class ExpertSystem:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def infer_backward(self, goal, visited=None):
        if visited is None:
            visited = set()
        
        if goal in visited:
            return False
        visited.add(goal)

        if goal in self.facts:
            return True

        applicable_rules = [r for r in self.rules if r['consequent'] == goal]
        if not applicable_rules:
            response = input(f"Does the animal have '{goal}'? (y/n): ").strip().lower()
            if response == 'y':
                self.facts.add(goal)
                return True
            else:
                return False

        for rule in applicable_rules:
            all_met = True
            for cond in rule['antecedent']:
                if not self.infer_backward(cond, visited.copy()):
                    all_met = False
                    break
            if all_met:
                self.facts.add(goal)
                return True
        return False


if __name__ == "__main__":
    system = ExpertSystem()

    # initial known facts
    system.add_fact("has_fur")
    system.add_fact("eats_meat")
    system.add_fact("has_tawny_color")
    system.add_fact("has_dark_spots")

    # rules
    system.add_rule({"antecedent": ["has_fur", "eats_meat", "has_tawny_color", "has_dark_spots"], "consequent": "cheetah"})
    system.add_rule({"antecedent": ["has_fur", "eats_meat", "has_tawny_color", "has_black_stripes"], "consequent": "tiger"})
    system.add_rule({"antecedent": ["has_feather", "can_fly", "lay_eggs"], "consequent": "bird"})
    system.add_rule({"antecedent": ["mammal"], "consequent": "has_fur"})
    system.add_rule({"antecedent": ["mammal", "has_hooves"], "consequent": "ungulate"})

    goal = input("Enter the animal to identify: ").strip().lower()
    result = system.infer_backward(goal)
    print(f"\nConclusion: The hypothesis that it is a '{goal}' is {result}.")
    print(f"Final set of facts: {system.facts}")
