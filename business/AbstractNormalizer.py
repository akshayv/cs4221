from business import KeysRetriever
from domain.FunctionalDependency import FunctionalDependency
from domain.Key import Key
import itertools
from domain.Relation import Relation

__author__ = 'akshay'


class AbstractNormalizer:
    def __init__(self):
        pass

    @staticmethod
    def separate_functional_deps(functional_deps):
        separated_functional_deps = set()
        for functional_dep in functional_deps:
            if len(functional_dep.rhs_attributes) > 1:
                for rhs_attribute in functional_dep.rhs_attributes:
                    separated_functional_deps.add(
                        FunctionalDependency(functional_dep.lhs_attributes, set(rhs_attribute)))
            else:
                separated_functional_deps.add(functional_dep)
        return separated_functional_deps

    @staticmethod
    # added a second and third argument for uniformity
    def is_trivial(functional_dep, keys=None, elementary_keys=None):
        return len(functional_dep.rhs_attributes - functional_dep.lhs_attributes) == 0

    @staticmethod
    def is_x_superkey(functional_dep, candidate_keys, elementary_keys=None):
        for candidate_key in candidate_keys:
            if len(candidate_key.attributes - functional_dep.lhs_attributes) == 0:
                return True
        return False

    @staticmethod
    def is_prime_attribute(functional_dep, candidate_keys, elementary_keys=None):
        for rhs_attribute in functional_dep.rhs_attributes:
            is_cur_rhs_prime = False
            for candidate_key in candidate_keys:
                if rhs_attribute in candidate_key.attributes:
                    is_cur_rhs_prime = True
                    break
            if is_cur_rhs_prime:
                continue
            else:
                return False
        return True


    @staticmethod
    def is_elementary_prime_attribute(functional_dep, candidate_keys, elementary_keys):
        for rhs_attribute in functional_dep.rhs_attributes:
            is_cur_rhs_elementary_prime = False
            for elementary_key in elementary_keys:
                if rhs_attribute in elementary_key.attributes:
                    is_cur_rhs_elementary_prime = True
                    break
            if is_cur_rhs_elementary_prime:
                continue
            else:
                return False
        return True


    @staticmethod
    def is_x_not_proper_subset(functional_dep, candidate_keys, elementary_keys=None):
        for candidate_key in candidate_keys:
            if functional_dep.lhs_attributes != candidate_key.attributes and len(
                            functional_dep.lhs_attributes - candidate_key.attributes) == 0:
                return False
        return True

    @staticmethod
    def binary_decompose(relation, offending_functional_dep):
        closure_x = KeysRetriever.find_closure(offending_functional_dep.lhs_attributes, relation.functional_deps)
        relation1 = Relation(closure_x,
                             AbstractNormalizer.get_matching_functional_deps(closure_x, relation.functional_deps))
        relation1.primary_key = offending_functional_dep.lhs_attributes
        remaining_attributes = set(relation.attributes - closure_x).union(offending_functional_dep.lhs_attributes)
        relation2 = Relation(remaining_attributes,
                             AbstractNormalizer.get_matching_functional_deps(remaining_attributes,
                                                                             relation.functional_deps))
        return [relation1, relation2]

    @staticmethod
    def get_matching_functional_deps(attributes_subset, all_functional_deps):
        matching_functional_deps = []
        for functional_dep in all_functional_deps:
            if len(functional_dep.lhs_attributes - attributes_subset) == 0 and len(
                            functional_dep.rhs_attributes - attributes_subset) == 0:
                matching_functional_deps.append(functional_dep)
        return matching_functional_deps

    @staticmethod
    def normalize(relation, requirements):
        relation.functional_deps = AbstractNormalizer.expand_functional_deps(relation.functional_deps,
                                                                             relation.attributes)
        relations = [relation]
        iterator = 0
        while iterator < len(relations):
            cur_relation = relations[iterator]
            keys = KeysRetriever.retrieve_candidate_keys(cur_relation.functional_deps, cur_relation.attributes)
            elementary_keys = KeysRetriever.retrieve_elementary_candidate_keys(cur_relation.functional_deps, keys)
            cur_relation.elementary_keys = elementary_keys
            cur_relation.keys = keys
            if cur_relation.primary_key is None:
                cur_relation.primary_key = next(iter(keys))
            for functional_dep in cur_relation.functional_deps:
                requirement_met = False
                for requirement in requirements:
                    if requirement(functional_dep, keys, elementary_keys):
                        requirement_met = True
                        break
                if not requirement_met:
                    decomposed_relations = AbstractNormalizer.binary_decompose(cur_relation, functional_dep)
                    relations[iterator] = decomposed_relations[0]
                    relations.append(decomposed_relations[1])
                    iterator -= 1
                    break
            iterator += 1
        return relations

    @staticmethod
    def expand_functional_deps(functional_deps, attributes):
        functional_deps_list = []
        all_subsets = AbstractNormalizer.find_all_subsets(attributes)
        all_subsets.sort(lambda x, y: cmp(len(x), len(y)))
        for subset in all_subsets:
            closure = KeysRetriever.find_closure(subset, functional_deps)
            functional_deps_list.append(FunctionalDependency(set().union(subset), closure))

        functional_deps_list = list(AbstractNormalizer.separate_functional_deps(functional_deps_list))
        functional_deps_list.sort(lambda x, y: cmp(len(x.lhs_attributes), len(y.lhs_attributes)))

        # Remove duplicates, redundant and trivial
        i = 0
        while i < len(functional_deps_list):
            dep_i = functional_deps_list[i]
            j = 0

            if len(dep_i.rhs_attributes - dep_i.lhs_attributes) == 0:
                functional_deps_list.pop(i)
                continue
            while j < len(functional_deps_list):
                dep_j = functional_deps_list[j]
                if i != j and (dep_j.lhs_attributes == dep_i.lhs_attributes and dep_j.rhs_attributes == dep_i.rhs_attributes):
                    functional_deps_list.pop(j)
                if i < j and len(dep_j.lhs_attributes.intersection(dep_i.lhs_attributes)) is not 0 \
                        and dep_i.rhs_attributes == dep_j.rhs_attributes:
                    functional_deps_list.pop(j)
                j += 1
            i += 1
        return functional_deps_list


    @staticmethod
    def find_all_subsets(attributes_set):
        all_subsets = []
        for i in range(1, len(attributes_set) + 1):
            all_subsets.extend(set(itertools.combinations(attributes_set, i)))
        return all_subsets


if __name__ == "__main__":
    # Test separate functional dependencies method
    print "\nTest separate_functional_deps"
    functional_deps = [FunctionalDependency({'a', 'b'}, {'c', 'd'}), FunctionalDependency({'c', 'e'}, {'c'})]
    print AbstractNormalizer.separate_functional_deps(functional_deps)

    # Test prime attribute method
    print "\nTest is_prime_attribute (expected False, True)"
    print AbstractNormalizer.is_prime_attribute(FunctionalDependency({}, {'e'}), [Key({'a', 'b'}), Key({'c', 'd'})])
    print AbstractNormalizer.is_prime_attribute(FunctionalDependency({}, {'a', 'c'}),
        [Key({'a', 'b'}), Key({'c', 'd'})])

    # Test is functional dependency trivial method
    print "\nTest is_trivial (expected True, False, False, True)"
    print AbstractNormalizer.is_trivial(FunctionalDependency({'a', 'c', 'b'}, {'a', 'c'}), {})
    print AbstractNormalizer.is_trivial(FunctionalDependency({'a', 'b', 'c'}, {'c', 'd', 'b'}), {})
    print AbstractNormalizer.is_trivial(FunctionalDependency({'a'}, {'a', 'b'}), {})
    print AbstractNormalizer.is_trivial(FunctionalDependency({'a', 'b'}, {'a'}), {})

    # Test is superkey method
    print "\nTest is_x_superkey (expected True, False, False)"
    print AbstractNormalizer.is_x_superkey(FunctionalDependency({'a', 'b', 'c'}, {}),
                                           [Key({'a', 'b'}), Key({'c', 'd'})])
    print AbstractNormalizer.is_x_superkey(FunctionalDependency({'a', 'c'}, {}), [Key({'a', 'b'}), Key({'c', 'd'})])
    print AbstractNormalizer.is_x_superkey(FunctionalDependency({'a', }, {}), [Key({'a', 'b'}), Key({'c', 'd'})])