from enum import Enum

class Group(Enum):
    rock = "rock"
    paper = "paper"
    scissor = "scissor"
    
    @staticmethod
    def compare(self_group: 'Group', target_group: 'Group'):
        self_group_name = self_group.name
        
        match self_group_name:
            case "rock":
                if (target_group == Group.rock):
                    return 0
                elif (target_group == Group.paper):
                    return -1
                elif(target_group == Group.scissor):
                    return 1
            case "paper":
                if (target_group == Group.rock):
                    return 1
                elif (target_group == Group.paper):
                    return 0
                elif(target_group == Group.scissor):
                    return -1
            case "scissor":
                if (target_group == Group.rock):
                    return -1
                elif (target_group == Group.paper):
                    return 1
                elif(target_group == Group.scissor):
                    return 0