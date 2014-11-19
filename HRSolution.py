from __future__ import print_function
from collections import deque
from HRBoard import HRBoard

class HRSolution:
    def __init__(self, board):
        self.steps = deque()
        self.init_layout = []
        self.init_board = board
    def clear(self):
        self.steps.clear()

    def populate(self, final_node):
        n = final_node
        while n:
            self.steps.appendleft(n)
            n = n.parent
        self.init_layout = self.steps.popleft().hash_code
        #self.init_board.dehash_board(self.init_layout)
        return self.init_layout

    def _output_moves(self, results_per_line, step_iter, step_wid = 2):
        n_steps = len(self.steps)
        i_step = -1
        while True:
            line_start_i_step =  i_step + 1
            prompt_str = 'Step {0:{1}}'.format(line_start_i_step+1, step_wid)
            step_str_list = []
            for i in range(results_per_line):   # Read n lines
                try:
                    i_step, this_step = next(step_iter)
                except StopIteration:
                    break
                step_str_list.append(str(this_step))
            step_str = ' --> '.join(step_str_list)

            if results_per_line > 1:     # If there should be more than one elem in each row
                prompt_str += ' to {0:{1}}:\n  '.format(i_step+1, step_wid)
            else:
                prompt_str += ':  '

            if i_step == n_steps - 1:   # If this happens to be the last step
                print(prompt_str + step_str)
                break              # Then we are done
            else:
                print(prompt_str + step_str + ' --> ')

    def _output_graphical(self, results_per_line, step_iter, step_wid = 2):
        n_steps = len(self.steps)
        i_step = -1
        while True:
            line_start_i_step =  i_step + 1
            prompt_str = 'Step {0:{1}}'.format(line_start_i_step+1, step_wid)
            step_str_list = []
            for i in range(results_per_line):   # Read n lines
                try:
                    i_step, this_step = next(step_iter)
                except StopIteration:
                    break

                step_str_list.append(str(this_step))
            step_str = ' --> '.join(step_str_list)

            if results_per_line > 1:     # If there should be more than one elem in each row
                prompt_str += ' to {0:{1}}:\n  '.format(i_step+1, step_wid)
            else:
                prompt_str += ':  '

            if i_step == n_steps - 1:   # If this happens to be the last step
                print(prompt_str + step_str)
                break              # Then we are done
            else:
                print(prompt_str + step_str + ' --> ')

    def output(self,  results_per_line = 4, if_graphical=False, dir_shorthand=False):
        print("\nSolution Report:")
        print("="*40)
        print("Initial Layout:")
        print("-"*40)
        self.init_board.show_board()
        print()
        print("Solution:")
        print("-"*40)
        n_steps = len(self.steps)
        res_line = []
        #if dir_shorthand:

        #else:
        #    to_str = s.__repr__
        step_wid = 2 if n_steps < 100 else 3
        step_iter = enumerate(self.steps)
        i_step = -1

        self._output_moves(results_per_line, step_iter, step_wid)
        # for i, s in enumerate(self.steps):
        #     if i % results_per_line == 0:   # For every nth line (n == results_per_line)
        #         print('Step {0:{1}}'.format(i+1, step_wid), end = '')
        #         last_step_on_line = min(i+results_per_line, n_steps)
        #         print(' to {0:{1}}:\n '.format(last_step_on_line, step_wid) if results_per_line > 1 else ': ',
        #                     end=' ')
        #     if not if_graphical:    # Using only DESCRIPTIONS of moves
        #
        #         print(s, end=' ')
        #         if i != n_steps-1:
        #             print('-->', end=' ')
        #             if (i+1) % results_per_line == 0:
        #                 print()
        #     else:   # Output board layout after every step, along with the description
        #

        print()
        print("-"*40)

        print("Total steps: {0}".format(n_steps))
        print("{0:=^40}".format(" END OF REPORT "))   # -"*15 + "END OF REPORT" + "-"*15)
        #print("{0}".format(self.init_layout))
