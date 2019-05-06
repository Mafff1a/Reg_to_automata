# -*- coding: utf-8 -*-
from graphviz import Digraph
from Tkinter import *

ope = ('|', '*', '(', ')')


# 自动机基类
class Automata:
    """class to represent an Automata"""

    # 初始化状态list
    def __init__(self, language=set(['0', '1'])):
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language

    # epsilon
    @staticmethod
    def epsilon():
        return ":e:"

    # 所见即所得
    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate: inp}

    # 从dict增加transition
    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    # get e-close龙书NFA->DFA理论(只通过e可以到达的状态)
    def getEClose(self, findstate):
        allstates = set()
        states = set([findstate])
        while len(states) != 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def display(self):
        print "states:", self.states
        print "start state: ", self.startstate
        print "final states:", self.finalstates
        print "transitions:"
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print "  ", fromstate, "->", state, "on '" + char + "'",
            print

    def NFA_To_SVG(self):
        nfagraph = Digraph("nfa", format="svg", engine="dot")
        nfagraph.attr(rankdir="LR")
        notenum = 1
        for each in self.states:
            if each in self.finalstates:
                nfagraph.node(str(each), label=str(notenum), shape="doublecircle")
                notenum += 1
            else:
                nfagraph.node(str(each), label=str(notenum))
                notenum += 1
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    if char == ':e:':
                        nfagraph.edge(str(fromstate), str(state), label=u'ε')
                    else:
                        nfagraph.edge(str(fromstate), str(state), label=str(char))
        nfagraph.render('nfa.svg', view=True)

    def DFA_To_SVG(self):
        nfagraph = Digraph("dfa", format="svg", engine="dot")
        nfagraph.attr(rankdir="LR")
        notenum = 1
        for each in self.states:
            if each in self.finalstates:
                nfagraph.node(str(each), label=str(notenum), shape="doublecircle")
                notenum += 1
            else:
                nfagraph.node(str(each), label=str(notenum))
                notenum += 1
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    if char == ':e:':
                        nfagraph.edge(str(fromstate), str(state), label=u'ε')
                    else:
                        nfagraph.edge(str(fromstate), str(state), label=str(char))
        nfagraph.render('DFA.svg', view=True)

    def MINDFA_To_SVG(self):
        nfagraph = Digraph("mindfa", format="svg", engine="dot")
        nfagraph.attr(rankdir="LR")
        notenum = 1
        for each in self.states:
            if each in self.finalstates:
                nfagraph.node(str(each), label=str(notenum), shape="doublecircle")
                notenum += 1
            else:
                nfagraph.node(str(each), label=str(notenum))
                notenum += 1
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    if char == ':e:':
                        nfagraph.edge(str(fromstate), str(state), label=u'ε')
                    else:
                        nfagraph.edge(str(fromstate), str(state), label=str(char))
        nfagraph.render('MINDFA.svg', view=True)

    def getPrintText(self):
        text = "language: {" + ", ".join(self.language) + "}\n"
        text += "states: {" + ", ".join(map(str, self.states)) + "}\n"
        text += "start state: " + str(self.startstate) + "\n"
        text += "final states: {" + ", ".join(map(str, self.finalstates)) + "}\n"
        text += "transitions:\n"
        linecount = 5
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    text += "    " + str(fromstate) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount += 1
        return [text, linecount]

    # 重编结点编号
    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    # 等价状态的合并(龙书)
    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartstate(pos[self.startstate])
        for s in self.finalstates:
            rebuild.addfinalstates(pos[s])
        return rebuild

    # just for debug
    def DebugLanguage(self):
        print self.language


class BuildAutomata:
    """class for building e-nfa basic structures"""

    @staticmethod
    # 基础结构
    def basicstruct(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setstartstate(state1)
        basic.addfinalstates(state2)
        basic.addtransition(1, 2, inp)
        return basic

    @staticmethod
    # or操作
    def plusstruct(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    # link
    @staticmethod
    def dotstruct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2 - 1
        dot = Automata()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, Automata.epsilon())
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    # 闭包
    @staticmethod
    def starstruct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, Automata.epsilon())
        star.addtransition(star.startstate, star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], a.startstate, Automata.epsilon())
        star.addtransition_dict(a.transitions)
        return star


class NFAfromRegex:
    """class for building e-nfa from regular expressions"""

    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.alphabet.extend([chr(i) for i in range(97, 123)])
        self.alphabet.extend([chr(i) for i in range(48, 58)])
        self.buildNFA()

    def getNFA(self):
        return self.nfa

    def displayNFA(self):
        self.nfa.DFA_To_SVG()

    def tosvg(self):
        self.nfa.NFA_To_SVG()

    def DEBUGLANG(self):
        print self.nfa.language

    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        # 扫描RE的过程类似于使用双栈表达式求表达式
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                # 读入单个字符
                language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildAutomata.basicstruct(char))
            # 默认括号左边是连接别的东西
            elif char == self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char == self.closingBracket:
                # 右括号左边只能加闭包
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                # 弹弹弹直到遇到对的那个左括号
                while (1):
                    if len(self.stack) == 0:
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            # 只有在alphabet里面的后面才能跟闭包
            elif char == self.star:
                if previous in self.operators or previous == self.openingBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous == self.openingBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print self.automata
            raise BaseException("Regex could not be parsed successfully")
        self.nfa = self.automata.pop()
        self.nfa.language = language

    def addOperatorToStack(self, char):
        while (1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack) - 1]
            # 左括号代表遇到了封闭内容，先入栈先
            if top == self.openingBracket:
                break
            # 不是的话，先处理一下前面的符号
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    # 按照ope对应的结果进行构建即可
    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error processing operator '%s'. Stack is empty" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b, a))
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b, a))


class DFAfromNFA:
    """class for building dfa from e-nfa and minimise it"""

    def __init__(self, nfa):
        self.buildDFA(nfa)
        self.minimise()

    def getDFA(self):
        return self.dfa

    def getMinimisedDFA(self):
        return self.minDFA

    def displayDFA(self):
        self.dfa.display()
        self.dfa.DFA_To_SVG()

    def displayMinimisedDFA(self):
        self.minDFA.display()
        self.minDFA.MINDFA_To_SVG()

    # todo debug
    def buildDFA(self, nfa):
        allstates = dict()
        # e-closeure
        eclose = dict()
        count = 1
        """
         龙书(中文版)p.97 先对开始状态s0进行初始化
         然后while(在Dstates中有一个未标记状态)
         进行e-closure建造
         
         
         """

        state1 = nfa.getEClose(nfa.startstate)
        eclose[nfa.startstate] = state1
        # 初始化DFA
        dfa = Automata(nfa.language)
        dfa.setstartstate(count)
        states = [[state1, count]]
        allstates[count] = state1
        # 计数
        count += 1
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in dfa.language:
                trstates = nfa.gettransitions(state, char)
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = nfa.getEClose(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in allstates.values():
                        states.append([trstates, count])
                        allstates[count] = trstates
                        toindex = count
                        count += 1
                    else:
                        toindex = [k for k, v in allstates.iteritems() if v == trstates][0]
                    dfa.addtransition(fromindex, toindex, char)
        for value, state in allstates.iteritems():
            if nfa.finalstates[0] in state:
                dfa.addfinalstates(value)
        self.dfa = dfa

    # DFA模拟RE
    def acceptsString(self, string):
        currentstate = self.dfa.startstate
        for ch in string:
            if ch == ":e:":
                continue
            st = list(self.dfa.gettransitions(currentstate, ch))
            if len(st) == 0:
                return False
            currentstate = st[0]
        if currentstate in self.dfa.finalstates:
            return True
        return False

    def minimise(self):
        states = list(self.dfa.states)
        n = len(states)
        unchecked = dict()
        count = 1
        distinguished = []
        # 寻找等价结点
        equivalent = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states, range(len(states))))
        for i in range(n - 1):
            for j in range(i + 1, n):
                if not ([states[i], states[j]] in distinguished or [states[j], states[i]] in distinguished):
                    if (states[i] in self.dfa.finalstates and states[j] not in self.dfa.finalstates) or (states[i] not in self.dfa.finalstates and states[j] in self.dfa.finalstates):
                        distinguished.append([states[i], states[j]])
                        continue
                    eq = 1
                    toappend = []
                    for char in self.dfa.language:
                        s1 = self.dfa.gettransitions(states[i], char)
                        print "debug trans "
                        print s1
                        s2 = self.dfa.gettransitions(states[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("Multiple transitions detected in DFA")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in distinguished or [s2, s1] in distinguished:
                                eq = 0
                                break
                            else:
                                toappend.append([s1, s2, char])
                                eq = -1
                    if eq == 0:
                        distinguished.append([states[i], states[j]])
                    elif eq == -1:
                        s = [states[i], states[j]]
                        s.extend(toappend)
                        unchecked[count] = s
                        count += 1
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equivalent.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalent[p1] = equivalent[p1].union(st)
        newFound = True
        # 若找到等价结点，创建一个替代的结点
        while newFound and len(unchecked) > 0:
            newFound = False
            toremove = set()
            for p, pair in unchecked.items():
                for tr in pair[2:]:
                    if [tr[0], tr[1]] in distinguished or [tr[1], tr[0]] in distinguished:
                        unchecked.pop(p)
                        distinguished.append([pair[0], pair[1]])
                        newFound = True
                        break
        for pair in unchecked.values():
            p1 = pos[pair[0]]
            p2 = pos[pair[1]]
            if p1 != p2:
                st = equivalent.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalent[p1] = equivalent[p1].union(st)
        if len(equivalent) == len(states):
            self.minDFA = self.dfa
        else:
            self.minDFA = self.dfa.newBuildFromEquivalentStates(equivalent, pos)


"""re = raw_input()
nfa = NFAfromRegex(re)
nfa.displayNFA()

ob = nfa.getNFA()
ob.NFA_To_SVG()
fuck = DFAfromNFA(ob)
fuck.displayDFA()

fuck.displayMinimisedDFA()
"""