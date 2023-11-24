class Stack:

    def __init__(self):

        self.items = []



    def isEmpty(self):

        return len(self.items) == 0



    def push(self, item):

        self.items.append(item)



    def pop(self):

        if not self.isEmpty():

            return self.items.pop()

        else:

            raise IndexError("Pop from an empty stack")



    def peek(self):

        if not self.isEmpty():

            return self.items[-1]

        else:

            raise IndexError("Peek on an empty stack")



    def size(self):

        return len(self.items)



if __name__ == "__main__":

    pass
