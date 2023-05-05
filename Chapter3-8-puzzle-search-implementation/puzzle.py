class Puzzle:
    heuristic=None
    evaluation_function=None
    needs_hueristic=False
    num_of_instances=0
    def __init__(self,size,state,parent,action,path_cost,needs_hueristic=False):
        self.size = size
        goal_state = [it for it in range(1,size**2)]
        goal_state.append(0)
        self.goal_state = goal_state
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])


    def generate_heuristic(self):
        self.heuristic=0
        size = self.size
        for num in range(1,size**2):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/size)
            j=int(distance%size)
            self.heuristic=self.heuristic+i+j


    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j,size):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == (size-1):  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == (size-1):
            legal_action.remove('R')
        return legal_action

    def generate_child(self):
        size = self.size
        children=[]
        x = self.state.index(0)
        i = int(x / size)
        j = int(x % size)
        legal_actions=self.find_legal_actions(i,j,size)


        for action in legal_actions:
            new_state = self.state.copy()
            if action is 'U':
                new_state[x], new_state[x-size] = new_state[x-size], new_state[x]
            elif action is 'D':
                new_state[x], new_state[x+size] = new_state[x+size], new_state[x]
            elif action is 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(size,new_state,self,action,1,self.needs_hueristic))

        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution
