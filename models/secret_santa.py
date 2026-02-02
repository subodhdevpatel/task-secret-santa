from typing import List, Dict, Any

class SecretSanta:
    """
    Model to handle Secret Santa assignments logic
    """
    
    @staticmethod
    def assign_santa(employeeList: List[Dict[str, Any]], previousAssignments: List[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Assigns Secret Santas based on current employees and previous years' pairs.
        
        Constraints:
        1. No self-assignment.
        2. No repeat of last year's assignment.
        3. One gift giver per receiver and vice versa.
        
        Returns:
            A list of dictionary pairings or an empty list if no solution exists.
        """
        if not employeeList:
            return []

        if len(employeeList) < 2:
            print("Error: At least 2 employees are required for Secret Santa.")
            return []

        n = len(employeeList)
        email_indexes = {i: emp['Employee_EmailID'] for i, emp in enumerate(employeeList)}

        # Build set of previous invalid pairs
        invalid_pairs = set()
        if previousAssignments:
            for entry in previousAssignments:
                santa = entry.get('Employee_EmailID')
                child = entry.get('Secret_Child_EmailID')
                if santa and child:
                    invalid_pairs.add((santa, child))

        # Build Adjacency list for the bipartite graph
        adj = SecretSanta._build_graph(n, email_indexes, invalid_pairs)

        # match[v] stores the santa index assigned to child index v
        match = [-1] * n 
        
        def find_match(uIdx: int, visitedNodes: List[bool]) -> bool:
            for vIdx in adj[uIdx]:
                if not visitedNodes[vIdx]:
                    visitedNodes[vIdx] = True
                    # If child vIdx is unmatched or the santa matched with vIdx can find another match
                    if match[vIdx] < 0 or find_match(match[vIdx], visitedNodes):
                        match[vIdx] = uIdx
                        return True
            return False

        matches_found = 0
        for u in range(n):
            visited = [False] * n
            if find_match(u, visited):
                matches_found += 1
        
        if matches_found < n:
            print("Error: Could not find a valid assignment for all employees due to strict constraints.")
            return []

        return SecretSanta._format_result(employeeList, match)

    @staticmethod
    def _build_graph(n: int, email_indexes: Dict[int, str], invalid_pairs: set) -> List[List[int]]:
        """Builds an adjacency list where adj[u] contains possible children for santa u."""
        adj = [[] for _ in range(n)]
        for u in range(n):
            santa_email = email_indexes[u]
            for v in range(n):
                child_email = email_indexes[v]
                if u != v and (santa_email, child_email) not in invalid_pairs:
                    adj[u].append(v)
        return adj

    @staticmethod
    def _format_result(employeeList: List[Dict[str, Any]], match: List[int]) -> List[Dict[str, str]]:
        """Formats the matching indices into the final dictionary format."""
        result = []
        for child_idx, santa_idx in enumerate(match):
            santa = employeeList[santa_idx]
            child = employeeList[child_idx]
            result.append({
                'Employee_Name': santa['Employee_Name'],
                'Employee_EmailID': santa['Employee_EmailID'],
                'Secret_Child_Name': child['Employee_Name'],
                'Secret_Child_EmailID': child['Employee_EmailID']
            })
        return result
