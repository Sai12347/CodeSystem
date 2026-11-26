class Solution:
    def applyUndoRedo(self, commands: List[str]) -> str:
        undo_stack = []
        redo_stack = []
        for cmd in commands:
            if cmd == "UNDO":
                if undo_stack:
                    redo_stack.append(undo_stack.pop())
            elif cmd == "REDO":
                if redo_stack:
                    undo_stack.append(redo_stack.pop())
            else:
                undo_stack.append(cmd[5:])
                redo_stack.clear()
        return "".join(undo_stack)
