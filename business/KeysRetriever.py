from domain.FunctionalDependency import FunctionalDependency
from domain.Key import Key

__author__ = 'akshay'


def retrieve_candidate_keys(functional_deps, attributes):
    keys = []
    if len(attributes) == 0:
        return keys

    all_rhs_attributes = set()
    all_lhs = []
    for functional_dep in functional_deps:
        all_rhs_attributes.update(functional_dep.rhs_attributes)
        all_lhs.append(set(functional_dep.lhs_attributes))
    only_rhs_attributes = attributes - all_rhs_attributes

    for lhs in all_lhs:
        lhs.update(only_rhs_attributes)
        closure = find_closure(lhs, functional_deps)
        lhs.update(attributes - closure)
        keys.append(Key(lhs))

    if len(keys) == 0:
        keys.append(Key(attributes))

    # Sort based on size
    keys.sort(lambda x, y: cmp(len(x), len(y)))

    candidate_keys = []

    # Remove extra keys
    for key in keys:
        subset_key_exists = False
        for candidate_key in candidate_keys:
            if len(candidate_key.attributes - key.attributes) == 0:
                subset_key_exists = True
                break
        if not subset_key_exists:
            candidate_keys.append(key)

    return candidate_keys


def retrieve_elementary_candidate_keys(functional_deps, keys):
    elementary_candidate_keys = set()
    for key in keys:
        is_elementary_candidate_key = False
        for functional_dep in functional_deps:
            if functional_dep.lhs_attributes == key:
                is_elementary_candidate_key = True
                for inner_functional_dep in functional_deps:
                    if inner_functional_dep.lhs_attributes != functional_dep.lhs_attributes and len(
                                    functional_dep.lhs_attributes - inner_functional_dep.lhs_attributes) == 0:
                        is_elementary_candidate_key = False
        if is_elementary_candidate_key:
            elementary_candidate_keys.add(key)
    return elementary_candidate_keys


def find_closure(attributes_subset, functional_deps):
    closure = set()
    functional_deps_list = []

    functional_deps_list.extend(functional_deps)
    closure.update(attributes_subset)

    i = 0
    while i < len(functional_deps_list):
        dep = functional_deps_list[i]
        if len(dep.lhs_attributes - closure) == 0:
            before_update_size = len(closure)
            closure.update(dep.rhs_attributes)
            after_update_size = len(closure)
            if after_update_size > before_update_size:
                i = 0
                continue
        i += 1
    return closure


if __name__ == "__main__":
    print "Test retrieve_candidate_keys"

    print retrieve_candidate_keys({FunctionalDependency({'a', 'b'}, {'f'}), FunctionalDependency({'a', 'c'}, {'g'}),
                                   FunctionalDependency({'a', 'd'}, {'b'}), FunctionalDependency({'a', 'e'}, {'h'}),
                                   FunctionalDependency({'b'}, {'c'}), FunctionalDependency({'b'}, {'e'}),
                                   FunctionalDependency({'e'}, {'b'}),
                                   FunctionalDependency({'c'}, {'d'})}, {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'})
