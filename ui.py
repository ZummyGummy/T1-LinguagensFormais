import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from automata.dfa import DFA
from regexp.parser import RegexParser, RegexNode
from regexp.automaton import RegexToDFA
from automata.nfa import NFA
from regexp.test import *


class gui():

	def __init__(self):
		super().__init__()
		self.FA_list = []
		self.RE_list = []
		self.RL_list = []
		self.current_fa = None
		self.current_re = ''
		self.initUI()
		# self.window()

	def initUI(self):

		# main window
		self.main_window = QMainWindow()
		self.main_window.resize(800, 600)

		self.central_widget = QWidget()

		#layout
		self.grid = QGridLayout(self.central_widget)
		self.grid.setColumnStretch(1, 4)
		self.grid.setColumnStretch(2, 4)
		self.grid.setSpacing(5)
		# status bar
		self.main_window.statusBar()

		# -- menu bar --
		self.menubar = self.main_window.menuBar()
		self.menubar.setNativeMenuBar(False)

		# file bar actions
		self.file_menu = self.menubar.addMenu('&File')

		# menu bar Regular Language
		self.new_regular = QAction(QIcon('new.png'), '&New RL', self.main_window)
		self.new_regular.setShortcut('Ctrl+E')
		self.new_regular.setStatusTip('Criar nova linguagem regular')
		self.new_regular.triggered.connect(self.new_rl)
		self.file_menu.addAction(self.new_regular)

		# menu bar Automata
		self.new_automata = QAction(QIcon('new.png'), '&New FA', self.main_window)
		self.new_automata.setShortcut('Ctrl+N')
		self.new_automata.setStatusTip('Create novo autômato finito')
		self.new_automata.triggered.connect(self.new_fa)
		self.file_menu.addAction(self.new_automata)

		# menu bar Regular Expression
		self.new_expression = QAction(QIcon('new.png'), '&New RE', self.main_window)
		self.new_expression.setShortcut('Ctrl+Shift+N')
		self.new_expression.setStatusTip('Create nova expressão regular')
		self.new_expression.triggered.connect(self.new_re)
		self.file_menu.addAction(self.new_expression)

		self.exit_action = QAction(QIcon('exit.png'), '&Exit', self.main_window)
		self.exit_action.setShortcut('Ctrl+Q')
		self.exit_action.setStatusTip('Exit application')
		self.exit_action.triggered.connect(qApp.quit)
		self.file_menu.addAction(self.exit_action)

		# edit menu bar actions
		self.edit_menu = self.menubar.addMenu('&Edit')

		# FA options:
		self.new_state = QAction(QIcon('state.png'), '&Create State', self.main_window)
		self.new_state.setShortcut('Ctrl+S')
		self.new_state.setStatusTip('Creates new state to current FA')
		self.new_state.triggered.connect(self.create_state_event)
		self.edit_menu.addAction(self.new_state)

		self.delete_state = QAction(QIcon('state.png'), '&Delete State', self.main_window)
		self.delete_state.setShortcut('Ctrl+Shift+S')
		self.delete_state.setStatusTip('Deletes a state in current FA')
		self.delete_state.triggered.connect(self.delete_state_event)
		self.edit_menu.addAction(self.delete_state)

		self.change_alphabet = QAction(QIcon('state.png'), '&Edit Alphabet', self.main_window)
		self.change_alphabet.setShortcut('Ctrl+A')
		self.change_alphabet.setStatusTip('Changes the alphabet of current automata')
		self.change_alphabet.triggered.connect(self.change_alphabet_event)
		self.edit_menu.addAction(self.change_alphabet)

		self.add_final_state = QAction(QIcon('state.png'), '&Add state to finals', self.main_window)
		self.add_final_state.setShortcut('Ctrl+F')
		self.add_final_state.setStatusTip('Add a state to final set in current FA')
		self.add_final_state.triggered.connect(self.add_final_state_event)
		self.edit_menu.addAction(self.add_final_state)

		self.set_initial_state = QAction(QIcon('state.png'), '&Set Initial', self.main_window)
		self.set_initial_state.setShortcut('Ctrl+F')
		self.set_initial_state.setStatusTip('Set a state as initial of this AF')
		self.set_initial_state.triggered.connect(self.set_initial_state_event)
		self.edit_menu.addAction(self.set_initial_state)

		self.determinize = QAction(QIcon('state.png'), '&Determinize', self.main_window)
		self.determinize.setShortcut('Ctrl+Shift+D')
		self.determinize.setStatusTip('Determinizes the current FA')
		self.determinize.triggered.connect(self.determinize_event)
		self.edit_menu.addAction(self.determinize)

		self.minimize = QAction(QIcon('state.png'), '&Minimize', self.main_window)
		self.minimize.setShortcut('Ctrl+Shift+M')
		self.minimize.setStatusTip('Minimizes the current FA')
		self.minimize.triggered.connect(self.minimize_event)
		self.edit_menu.addAction(self.minimize)

		self.unite = QAction(QIcon('state.png'), '&Union', self.main_window)
		self.unite.setShortcut('Ctrl+U')
		self.unite.setStatusTip('Unites an FA with another one FA')
		self.unite.triggered.connect(self.union_event)
		self.edit_menu.addAction(self.unite)

		self.intersection = QAction(QIcon('state.png'), '&Intersection', self.main_window)
		self.intersection.setShortcut('Ctrl+I')
		self.intersection.setStatusTip('Intersects an FA with another one FA')
		self.intersection.triggered.connect(self.intersection_event)
		self.edit_menu.addAction(self.intersection)

		self.complement = QAction(QIcon('state.png'), '&Complement', self.main_window)
		self.complement.setShortcut('Ctrl+Shift+C')
		self.complement.setStatusTip('Complements current FA')
		self.complement.triggered.connect(self.complement_event)
		self.edit_menu.addAction(self.complement)

		self.diff = QAction(QIcon('state.png'), '&Difference', self.main_window)
		self.diff.setShortcut('Ctrl+Shift+C')
		self.diff.setStatusTip('Makes the difference of an FA with a second FA')
		self.diff.triggered.connect(self.diff_event)
		self.edit_menu.addAction(self.diff)

		self.edit_menu.addSeparator()

		# RE Options

		self.generate_automata = QAction(QIcon('state.png'), '&Generate Automata', self.main_window)
		self.generate_automata.setShortcut('Ctrl+G')
		self.generate_automata.setStatusTip('Creates the automata from this Regular Expression')
		self.generate_automata.triggered.connect(self.generate_automata_event)
		self.edit_menu.addAction(self.generate_automata)

		self.edit_expression = QAction(QIcon('state.png'), '&Edit Expression', self.main_window)
		self.edit_expression.setShortcut('Ctrl+E')
		self.edit_expression.setStatusTip('Edits the expression')
		self.edit_expression.triggered.connect(self.edit_expression_event)
		self.edit_menu.addAction(self.edit_expression)

		self.compare_expression = QAction(QIcon('state.png'), '&Compare Expression', self.main_window)
		self.compare_expression.setShortcut('Ctrl+Alt+C')
		self.compare_expression.setStatusTip('Determines if the expression is equal to target expression')
		self.compare_expression.triggered.connect(self.compare_expression_event)
		self.edit_menu.addAction(self.compare_expression)


		self.edit_menu.addSeparator()


		self.close = QAction(QIcon('state.png'), '&Close Tab', self.main_window)
		#self.close.setShortcut('Ctrl+S')
		self.close.setStatusTip('Closes current tb')
		self.close.triggered.connect(self.close_event)
		self.edit_menu.addAction(self.close)

		self.allow_FA(0)
		self.allow_RE(0)

		# tab

		self.tabs = QTabWidget(self.central_widget)
		self.tabs.resize(800,600)
		self.central_widget

		self.disable_changes = False

		self.tabs.currentChanged.connect(self.tab_changed)

		self.main_window.setCentralWidget(self.central_widget)

		self.main_window.setGeometry(300,300,800,600)
		self.main_window.show()

		#self.create_fa('m1', 'ab')
		#self.create_state('q0', True, True)
		#self.create_fa('m2', 'abc')

	def allow_FA(self, boolea):
		if boolea:
			self.allow_RE(False)
			self.determinize.setEnabled(True)
			self.minimize.setEnabled(True)
			self.diff.setEnabled(True)
			self.complement.setEnabled(True)
			self.intersection.setEnabled(True)
			self.unite.setEnabled(True)
			self.delete_state.setEnabled(True)
			self.new_state.setEnabled(True)
			self.close.setEnabled(True)
			self.add_final_state.setEnabled(True)
			self.set_initial_state.setEnabled(True)
			self.change_alphabet.setEnabled(True)
		else:
			self.determinize.setEnabled(False)
			self.minimize.setEnabled(False)
			self.diff.setEnabled(False)
			self.complement.setEnabled(False)
			self.intersection.setEnabled(False)
			self.unite.setEnabled(False)
			self.delete_state.setEnabled(False)
			self.new_state.setEnabled(False)
			self.close.setEnabled(False)
			self.add_final_state.setEnabled(False)
			self.set_initial_state.setEnabled(False)
			self.change_alphabet.setEnabled(False)

	def allow_RE(self, boolea):
		if boolea:
			self.allow_FA(False)
			self.generate_automata.setEnabled(True)
			self.edit_expression.setEnabled(True)
			self.compare_expression.setEnabled(True)
			self.close.setEnabled(True)

		else:
			self.generate_automata.setEnabled(False)
			self.edit_expression.setEnabled(False)
			self.compare_expression.setEnabled(False)
			self.close.setEnabled(False)

	def generate_automata_event(self):
		state_name, ok = QInputDialog.getText(self.main_window, 'Gerar Autômato', 'Dê um nome ao nomo autômato:')
		if ok:
			self.generate_automata_(state_name)

	def generate_automata_(self, automata_name):
		current_tab = self.tabs.currentWidget()
		name = current_tab.name
		print('Nome da Tab: ' + name)
		print('Expressão Regular atual: ' + self.current_re)
		for regular_expression in self.RE_list:
			if regular_expression[0] == name:
				self.current_re = regular_expression[1]
				print('Regular Expression changed: ' + self.current_re)

		tree = to_ast(self.current_re)
		converter = RegexToDFA()
		dfa = converter.convert(tree)

		self.FA_list.append(dfa)
		self.add_tab(dfa.name, ['FA', dfa.alphabet])

	def edit_expression_event(self):
		new_expression, ok = QInputDialog.getText(self.main_window, 'Edit Expression', 'New Expression:')
		if ok:
			current_tab = self.tabs.currentWidget()
			name = current_tab.name
			for regular_expression in self.RE_list:
				if regular_expression[0] == name:
					regular_expression[1] = new_expression
					current_re = new_expression
					print('Expression: ' + current_re)
					current_tab.label.setText('Regular Expression: ' + current_re)
					break

	def compare_expression_event(self):
		found = False
		while not found:
			expression, ok = QInputDialog.getText(self.main_window, 'Compare', 'What is the name of the second expression?')
			if ok:
				second_expression = ''
				for regular_expression in self.RE_list:
					if regular_expression[0] == expression:
						found = True
						second_expression = regular_expression[1]
						break
				if found:
					# result = equivalence(RE_Algorithms.de_simone(self.current_re), RE_Algorithms.de_simone(second_expression))
					if result:
						end = QMessageBox.question(self.main_window, 'Equal', 'The second expression is equal the first one', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					else:
						end = QMessageBox.question(self.main_window, 'Not Equal', 'The second expression is not equal the first one', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				else:
					again = QMessageBox.question(self.main_window, 'Not Found', 'The second expression was not found, try again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if again == QMessageBox.No:
						break

	def create_state_event(self):
		state_name, ok = QInputDialog.getText(self.main_window, 'Create State', 'Name the state:')
		if ok:
			is_final = QMessageBox.question(self.main_window, 'Final?', 'Is the state final?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			is_initial = QMessageBox.question(self.main_window, 'Final?', 'Is the state initial?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if is_initial == QMessageBox.Yes:
				is_initial = True
			else:
				is_initial = False
			if is_final == QMessageBox.Yes:
				is_final = True
			else:
				is_final = False
			self.create_state(state_name, is_final, is_initial)

	def create_state(self, state_name, is_final, is_initial):
		current_tab = self.tabs.currentWidget()
		if self.current_fa is None or self.current_fa.name != current_tab.name:
			for fa in self.FA_list:
				if fa.name == current_tab.name:
					self.current_fa = fa
					break
		self.current_fa.create_state(state_name, is_initial, is_final)
		self.update_table()

	def delete_state_event(self):
		delete_state_text, ok = QInputDialog.getText(self.main_window, 'Delete State', 'Name the state:')

		if ok:
			self.remove_state(delete_state_text)

	def remove_state(self, name):
		self.current_fa.delete_state(name)
		self.update_table()

	def change_alphabet_event(self):
		alphabet, ok = QInputDialog.getText(self.main_window, 'New Alphabet', 'New alphabet: ')
		if ok:
			current_tab = self.tabs.currentWidget()
			current_tab.characters.clear()
			for character in alphabet:
				current_tab.characters.append(character)
			current_tab.table_widget.setColumnCount(len(current_tab.characters))
			current_tab.table_widget.setHorizontalHeaderLabels(current_tab.characters)

	def add_final_state_event(self):
		final_state, ok = QInputDialog.getText(self.main_window, 'Final State', 'Name of the state:')

		if ok:
			self.add_final(final_state)

	def add_final(self, name):
		if name in self.current_fa.states:
			self.current_fa.add_final(name)
		self.update_table()

	def set_initial_state_event(self):
		initial_state, ok = QInputDialog.getText(self.main_window, 'Initial State', 'Name of the state:')

		if ok:
			self.set_initial(initial_state)

	def set_initial(self, name):
		if name in self.current_fa.states:
			self.current_fa.add_initial(name)
		self.update_table()

	def union_event(self):
		found = False
		while not found:
			union_text1, ok = QInputDialog.getText(self.main_window, 'Union', 'Name of the second automata:')
			if ok:
				found = False
				for automata in self.FA_list:
					if union_text1 == automata.name:
						found = True
						print('going to unite ' + self.current_fa.name + ' with ' + automata.name)
						self.unite_(self.current_fa, automata)
				if not found:
					again = QMessageBox.question(self.main_window, 'Not Found', 'The second automata was not found, try again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if again == QMessageBox.No:
						break

	def unite_(self, automata1, automata2):
		print("------Union------")
		print("Automata1: " + automata1.name)
		print('initial state: ' + automata1.initials)
		print('States:')
		print(automata1.states)
		print('Finals:')
		print(automata1.finals)
		print('Transitions: ')
		print(automata1.transitions)
		print('Alphabet: ')
		print(automata1.alphabet)

		print()
		print("Automata1: " + automata2.name)
		print('initial state: ' + automata2.initials)
		print('States:')
		print(automata2.states)
		print('Finals:')
		print(automata2.finals)
		print('Transitions: ')
		print(automata2.transitions)
		print('Alphabet: ')
		print(automata2.alphabet)
		new_fa = union(automata1, automata2)
		print('union done')
		new_fa.name = automata1.name + ' + ' + automata2.name
		print('name of new automata: ' + new_fa.name)
		new_fa.calculate_alphabet()

		self.FA_list.append(new_fa)

		print()
		print("Automata2: " + new_fa.name)
		print('initial state: ' + new_fa.initials)
		print('States:')
		print(new_fa.states)
		print('Finals:')
		print(new_fa.finals)
		print('Transitions: ')
		print(new_fa.transitions)
		print('Alphabet: ')
		print(new_fa.alphabet)
		self.add_tab(new_fa.name, ['FA', new_fa.alphabet])

	def intersection_event(self):
		found = False
		while not found:
			union_text1, ok = QInputDialog.getText(self.main_window, 'Intersection', 'Name of the second automata:')
			if ok:
				found = False
				for automata in self.FA_list:
					if union_text1 == automata.name:
						found = True
						print('going to intersect ' + self.current_fa.name + ' with ' + automata.name)
						self.intersect_(self.current_fa, automata)
				if not found:
					again = QMessageBox.question(self.main_window, 'Not Found', 'The second automata was not found, try again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if again == QMessageBox.No:
						break

	# def intersect_(self, automata1, automata2):
	# 	print("------Intersection------")
	# 	print("Automata1: " + automata1.name)
	# 	print('initial state: ' + automata1.initials)
	# 	print('States:')
	# 	print(automata1.states)
	# 	print('Finals:')
	# 	print(automata1.finals)
	# 	print('Transitions: ')
	# 	print(automata1.transitions)
	# 	print('Alphabet: ')
	# 	print(automata1.alphabet)
	#
	# 	print()
	# 	print("Automata1: " + automata2.name)
	# 	print('initial state: ' + automata2.initials)
	# 	print('States:')
	# 	print(automata2.states)
	# 	print('Finals:')
	# 	print(automata2.finals)
	# 	print('Transitions: ')
	# 	print(automata2.transitions)
	# 	print('Alphabet: ')
	# 	print(automata2.alphabet)
	# 	new_fa = intersection(automata1, automata2)
	# 	print('intersection done')
	# 	new_fa.name = automata1.name + ' v ' + automata2.name
	# 	print('name of new automata: ' + new_fa.name)
	# 	new_fa.calculate_alphabet()
	#
	# 	self.FA_list.append(new_fa)
	#
	# 	print()
	# 	print("Automata2: " + new_fa.name)
	# 	print('initial state: ' + new_fa.initials)
	# 	print('States:')
	# 	print(new_fa.states)
	# 	print('Finals:')
	# 	print(new_fa.finals)
	# 	print('Transitions: ')
	# 	print(new_fa.transitions)
	# 	print('Alphabet: ')
	# 	print(new_fa.alphabet)
	# 	self.add_tab(new_fa.name, ['FA', new_fa.alphabet])

	def complement_event(self):
		# temp_fa = complement(self.current_fa)
		# self.FA_list[self.FA_list.index(self.current_fa)] = temp_fa
		# self.current_fa = temp_fa
		self.update_table()

	def diff_event(self):
		found = False
		while not found:
			union_text1, ok = QInputDialog.getText(self.main_window, 'Difference', 'Name of the second automata:')
			if ok:
				found = False
				for automata in self.FA_list:
					if union_text1 == automata.name:
						found = True
						print('going to difference ' + self.current_fa.name + ' with ' + automata.name)
						self.diff_(self.current_fa, automata)
				if not found:
					again = QMessageBox.question(self.main_window, 'Not Found', 'The second automata was not found, try again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if again == QMessageBox.No:
						break

	def diff_(self, automata1, automata2):
		print("------Difference------")
		print("Automata1: " + automata1.name)
		print('initial state: ' + automata1.initials)
		print('States:')
		print(automata1.states)
		print('Finals:')
		print(automata1.finals)
		print('Transitions: ')
		print(automata1.transitions)
		print('Alphabet: ')
		print(automata1.alphabet)

		print()
		print("Automata1: " + automata2.name)
		print('initial state: ' + automata2.initials)
		print('States:')
		print(automata2.states)
		print('Finals:')
		print(automata2.finals)
		print('Transitions: ')
		print(automata2.transitions)
		print('Alphabet: ')
		print(automata2.alphabet)
		new_fa = dif(automata1, automata2)
		print('Diference done')
		new_fa.name = automata1.name + ' - ' + automata2.name
		print('name of new automata: ' + new_fa.name)
		new_fa.calculate_alphabet()

		self.FA_list.append(new_fa)

		print()
		print("Automata2: " + new_fa.name)
		print('initial state: ' + new_fa.initials)
		print('States:')
		print(new_fa.states)
		print('Finals:')
		print(new_fa.finals)
		print('Transitions: ')
		print(new_fa.transitions)
		print('Alphabet: ')
		print(new_fa.alphabet)
		self.add_tab(new_fa.name, ['FA', new_fa.alphabet])

	def minimize_event(self):
		# minimize(self.current_fa)
		self.update_table()
		'''new_fa = copy.copy(self.current_fa)
		minimize(new_fa)
		new_fa.name = 'min ' + new_fa.name
		new_fa.calculate_alphabet()
		self.FA_list.append(new_fa)
		self.add_tab(new_fa.name, ['FA', new_fa.alphabet])aa'''

	def determinize_event(self):
		# determinize(self.current_fa)
		self.update_table()
		'''new_fa = copy.copy(self.current_fa)
		determinize(new_fa)
		new_fa.name = 'det ' + new_fa.name
		new_fa.calculate_alphabet()
		self.FA_list.append(new_fa)
		self.add_tab(new_fa.name, ['FA', new_fa.alphabet])'''


	def new_rl(self):
		self.expression, ok = QInputDialog.getText(self.main_window, 'FA Input', 'Enter the name of the Regular Language: ')

		if ok:
			language, ok = QInputDialog.Te
		if ok:
			alphabet, ok = QInputDialog.getText(self.main_window, 'Entre com a expressão regular',
												'Enter the alphabet of ' + self.expression + '. (Example: abc)')

			self.create_rl(self.expression, alphabet)

	def create_rl(self, expression, alphabet):
		# new_FA = DFA()
		# new_FA.set_name(str(expression))
		# self.FA_list.append(new_FA)
		self.add_tab(expression, ['RL', alphabet])

	def new_fa(self):
		self.expression, ok = QInputDialog.getText(self.main_window, 'FA Input', 'Enter the name of the Finite Automata: ')
		if ok:
			alphabet, ok = QInputDialog.getText(self.main_window, 'Alphabet Input', 'Enter the alphabet of ' + self.expression + '. (Example: abc)')
			self.create_fa(self.expression, alphabet)

	def create_fa(self, expression, alphabet):
		automata = DFA()
		automata.set_name(str(expression))
		self.FA_list.append(automata)
		self.add_tab(expression, ['FA', alphabet])

	def new_re(self):
		name, ok = QInputDialog.getText(self.main_window, 'RE Input', 'Enter the name of the Regular Expression: ')
		if ok:
			self.expression, ok = QInputDialog.getText(self.main_window, 'RE Input', 'Enter the regular Expression: (Example: (a?|ba)* )')
			regular_expression = str(self.expression)
			self.create_re_(name, regular_expression)

	def create_re_(self, name, expression):
		self.RE_list.append([name, expression])
		self.current_re = expression
		self.add_tab(name, ['RE', expression])

	def cell_changed_event(self, row, column):
		if not self.disable_changes:
			current_tab = self.tabs.currentWidget()
			current_item = current_tab.table_widget.item(row, column)
			if current_item:
				text = current_item.text()
				# replace not working
				temp_tex = text.split(" ")
				text = ''
				for string in temp_tex:
					text += string
				print(text)
				if text != '' :
					self.current_fa.delete_all_transitions(current_tab.states[row], current_tab.characters[column])
					texts = text.split(',')
					print(texts)
					for new_text in texts:
						self.current_fa.create_transition(current_tab.states[row], new_text , current_tab.characters[column])
				else:
					self.current_fa.delete_all_transitions(current_tab.states[row], current_tab.characters[column])
				#might have added new state
				self.update_table()

	def update_table(self):
		current_tab = self.tabs.currentWidget()
		self.disable_changes = True
		current_tab.table_widget.setRowCount(len(self.current_fa.states))
		current_tab.states.clear()
		current_tab.states_extra.clear()
		name = ''
		for state in self.current_fa.states:
			name = state
			extra = ''
			if state in self.current_fa.finals:
				extra += '*'
			if state == self.current_fa.initials:
				extra += '->'
			current_tab.states.append(name)
			current_tab.states_extra.append(extra)
		names = list()
		i = 0
		while i < len(current_tab.states):
			names.append(current_tab.states_extra[i] + current_tab.states[i])
			i += 1
		current_tab.table_widget.setVerticalHeaderLabels(names)

		#update all cells with transitions:
		for index, state in enumerate(self.current_fa.states):
			if state in self.current_fa.transitions:
				keys = self.current_fa.transitions[state].keys()
				for key in keys:
					current_tab.table_widget.setItem(index, current_tab.characters.index(key), QTableWidgetItem(self.current_fa.transitions[state][key]))
		self.disable_changes = False

	def add_tab(self, tab_name, tab_type):
		new_tab = Tab(tab_name, tab_type)
		self.tabs.addTab(new_tab, tab_name)
		new_tab.table_widget.cellChanged.connect(self.cell_changed_event)

	# closes current tab
	def close_event(self):
		current_tab = self.tabs.currentWidget()
		self.tabs.removeTab(self.tabs.indexOf(current_tab))
		self.FA_list.remove(self.current_fa)

	# tab changed event
	def tab_changed(self):
		current_tab = self.tabs.currentWidget()
		if current_tab is not None:
			# FA
			if current_tab.type == 'FA':
				self.allow_FA(True)
				for fa in self.FA_list:
						if fa.name == current_tab.name:
							self.current_fa = fa
							break
				print()
				print("Current FA: " + self.current_fa.name)
				print('initial state: ' + self.current_fa.initials)
				print('States:')
				print(self.current_fa.states)
				print('Finals:')
				print(self.current_fa.finals)
				print('Transitions: ')
				print(self.current_fa.transitions)
				print('Alphabet: ')
				print(self.current_fa.alphabet)
				self.update_table()

			# RE
			if current_tab.type == 'RE':
				self.allow_RE(True)
				for regular_expression in self.RE_list:
					if regular_expression[0] == current_tab.name:
						self.current_re = regular_expression[1]
						break

			elif current_tab.type == 'RL':
				for regular_language in self.RL_list:
					if regular_language[0] == current_tab.name:
						self.current_rl = regular_language[1]
						break

	def window(self):
		app = QApplication(sys.argv)
		w = QWidget()
		w.setWindowTitle("Insira uma Linguagem Regular")
		w.resize(400, 400)

		textbox = QPlainTextEdit(w)
		textbox.resize(380, 300)
		textbox.move(10, 10)

		button = QPushButton("Ok", w)
		button.move(160, 320)

		button

		w.show()

		sys.exit(app.exec_())

# class InputText(QWindow):
#
# 	def __init__(self):
# 		self.app = QApplication(sys.argv)
# 		w = QWidget()
# 		w.setWindowTitle("Insira uma Linguagem Regular")
# 		w.resize(400, 400)
#
# 		textbox = QPlainTextEdit(w)
# 		textbox.resize(380, 300)
# 		textbox.move(10, 10)
#
# 		button = QPushButton("Ok", w)
# 		button.move(160, 320)
#
# 		button.conn
#
# 		w.show()
#
# 		sys.exit(app.exec_())


class Tab(QWidget):
	def __init__(self, tab_name, tab_type):
		super().__init__()
		self.name = tab_name
		self.type = tab_type[0]
		self.characters = list()
		self.table_widget = QTableWidget()
		self.states = list()
		self.states_extra = list()
		self.layout = QVBoxLayout(self)
		self.expression = ''
		self.label = QLabel()
		if self.type == 'FA':
			for character in tab_type[1]:
				self.characters.append(character)
			self.table_widget.setColumnCount(len(self.characters))
			self.table_widget.setHorizontalHeaderLabels(self.characters)
			self.layout.addWidget(self.table_widget)
		elif self.type == 'RE':
			self.expression = tab_type[1]
			self.label = QLabel('Regular Expression: ' + self.expression, self)
			self.layout.addWidget(self.label)
		self.setLayout(self.layout)

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = gui()
	sys.exit(app.exec_())
