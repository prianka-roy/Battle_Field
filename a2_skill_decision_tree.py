"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List
from a2_skills import RogueAttack, RogueSpecial, MageAttack, MageSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    def skills_that_pass(self, caster: 'Character', target: 'Character') ->list:
        """
        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> k = t.skills_that_pass('Mage', 'Rogue')
        >>> type(k) == list
        True
        """
        if self.children == []:
            return [self]
        if self.condition(caster, target) is False:
            return [self]

        return sum([child.skills_that_pass(caster, target)
                    for child in self.children], [])

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """ Returns picked skill from the SkillDecisionTree

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> k = t.pick_skill('Mage', 'Rogue')
        >>> type(k) == MageAttack
        True
        """

        c_list = self.skills_that_pass(caster, target)

        if len(c_list) == 1:
            return c_list[0].value

        priorities = []
        for c in c_list:
            priorities += [c.priority]

        max_p = min(priorities)

        skill_to_return = c_list[0]
        for i in c_list:
            if i.priority == max_p:
                skill_to_return = i

        return skill_to_return.value


def def_f(_, __) -> bool:
    """ Returns False"""

    return False

def f(caster: 'Character', _) -> bool:
    """ Returns if caster's hp  is greater than 50"""
    return caster.get_hp() > 50


def f3(caster: 'Character', _):
    """ Returns if casters sp is greatre than 20"""
    return caster.get_sp() > 20


def f4(_, target: 'Character'):
    """ Returns if target's hp is less than 30"""
    return target.get_hp() < 30


def f2(_, target: 'Character'):
    """ Returns if sp is greater than 40"""
    return target.get_sp() > 40


def f1(caster: 'Character', _):
    """ Returns if hp is greatre than 90"""
    return caster.get_hp() > 90


def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    """

    t6 = SkillDecisionTree(RogueAttack(), def_f, 6)

    t4 = SkillDecisionTree(RogueSpecial(), f4, 4)
    t4.children = [t6]

    t3 = SkillDecisionTree(MageAttack(), f3, 3)
    t3.children = [t4]

    t8 = SkillDecisionTree(RogueAttack(), def_f, 8)

    t2 = SkillDecisionTree(MageSpecial(), f2, 2)
    t2.children = [t8]

    t7 = SkillDecisionTree(RogueSpecial(), def_f, 7)

    t1 = SkillDecisionTree(RogueAttack(), f1, 1)
    t1.children = [t7]

    t = SkillDecisionTree(MageAttack(), f, 5)
    t.children = [t3, t2, t1]

    return t


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config='a2_pyta.txt')
