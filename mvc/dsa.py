# Stack implementation using a linked list.
# Node class
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    class EmptyStackError(Exception):
        def __init__(self, message="Peeking from an empty stack"):
            self.message = message
            super().__init__(self.message)

    # Initialize Stack using multiple data
    def __create(self, args):
        current = None
        for each in args:
            node = Node(each)
            self.size += 1
            if each == args[0]:
                self.head = node
            else:
                current.next = node
            current = node

    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self, *args):
        self.head = None
        self.size = 0
        self.__create(list(args))

    # String representation of the stack
    def __str__(self):
        cur = self.head
        out = ""
        while cur:
            if cur.next is not None:
                out += str(cur.value) + ", "
            else:
                out += str(cur.value)
            cur = cur.next
        return out

        # Get the current size of the stack

    def getSize(self):
        return self.size

    # Check if the stack is empty
    def isEmpty(self):
        return self.size == 0

    # Get the top item of the stack
    def peek(self):

        # Sanitary check to see if we
        # are peeking an empty stack.
        if self.isEmpty():
            raise self.EmptyStackError()
        return self.head.value

    # Push a value into the stack.
    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self.size += 1

    # Remove a value from the stack and return.
    def pop(self):
        if self.isEmpty():
            raise self.EmptyStackError()
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value

    # Make stack an array
    def toList(self):
        if self.isEmpty():
            return []
        else:
            lst = []
            current = self.head
            while current:
                lst.append(current.value)
                current = current.next
            return lst


class Sort:
    # Bubble sort algorithm
    @staticmethod
    def bubble_sort(array, key=None):
        n = len(array)
        returning_array = array
        # Traverse through all array elements
        for i in range(n - 1):
            # range(n) also work but outer loop will repeat one time more than needed.
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                isTrue = returning_array[j][key] > returning_array[j + 1][key] \
                    if key is not None else returning_array[j] > returning_array[j + 1]

                if isTrue:
                    returning_array[j], returning_array[j + 1] = returning_array[j + 1], returning_array[j]

        return returning_array

    @staticmethod
    def insertion_sort(arr, array_key=None):
        array = arr
        for i in range(1, len(array)):

            key = array[i]

            # Move elements of arr[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i - 1
            if array_key is not None:
                while j >= 0 and key[array_key] < array[j][array_key]:
                    array[j + 1] = array[j]
                    j -= 1
            else:
                while j >= 0 and key < array[j]:
                    array[j + 1] = array[j]
                    j -= 1
            array[j + 1] = key
        return array
