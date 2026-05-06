"""
Strategic AI for enemy combat decisions
Implements intelligent enemy behavior based on INT scores
"""
import random
from typing import Dict, List, Any


class EnemyAI:
    """Strategic AI for controlling enemies in combat"""
    
    def __init__(self, enemy_name: str, intelligence: int, hit_points: int, max_hp: int):
        self.name = enemy_name
        self.intelligence = intelligence
        self.hit_points = hit_points
        self.max_hp = max_hp
        self.morale = 100
        self.strategy = self._determine_strategy()
    
    def _determine_strategy(self) -> str:
        """Determine combat strategy based on intelligence"""
        if self.intelligence <= 5:
            return "berserker"  # Attack nearest, no tactics
        elif self.intelligence <= 10:
            return "basic"  # Simple tactics, focus fire
        elif self.intelligence <= 15:
            return "tactical"  # Use terrain, coordinate
        else:
            return "mastermind"  # Complex strategies, retreat when needed
    
    def should_retreat(self) -> bool:
        """Decide if enemy should retreat"""
        hp_percent = (self.hit_points / self.max_hp) * 100
        
        if self.strategy == "berserker":
            return False  # Never retreat
        elif self.strategy == "basic":
            return hp_percent < 10 and random.random() < 0.3
        elif self.strategy == "tactical":
            return hp_percent < 25 and random.random() < 0.6
        else:  # mastermind
            return hp_percent < 40 and random.random() < 0.8
    
    def choose_target(self, players: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Choose which player to target
        
        Args:
            players: List of player dicts with 'name', 'health', 'threat_level'
        
        Returns:
            Chosen target
        """
        if not players:
            return None
        
        if self.strategy == "berserker":
            # Attack nearest (random)
            return random.choice(players)
        
        elif self.strategy == "basic":
            # Focus fire on weakest
            return min(players, key=lambda p: p.get('health', 100))
        
        elif self.strategy == "tactical":
            # Target high threat or low health
            # 60% chance to target highest threat, 40% lowest health
            if random.random() < 0.6:
                return max(players, key=lambda p: p.get('threat_level', 0))
            else:
                return min(players, key=lambda p: p.get('health', 100))
        
        else:  # mastermind
            # Complex decision making
            # Consider threat, health, and position
            scores = []
            for player in players:
                score = 0
                
                # High threat = higher priority
                score += player.get('threat_level', 0) * 2
                
                # Low health = easier kill
                if player.get('health', 100) < 30:
                    score += 30
                
                # Healers are priority
                if 'cleric' in player.get('class', '').lower():
                    score += 20
                
                # Spellcasters are dangerous
                if any(c in player.get('class', '').lower() for c in ['wizard', 'sorcerer']):
                    score += 15
                
                scores.append((player, score))
            
            # Choose highest score
            return max(scores, key=lambda x: x[1])[0]
    
    def choose_action(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Choose what action to take
        
        Args:
            context: Combat context (allies, enemies, terrain, etc.)
        
        Returns:
            Action dict with 'type' and 'description'
        """
        # Check if should retreat
        if self.should_retreat():
            return {
                "type": "retreat",
                "description": f"{self.name} attempts to flee!"
            }
        
        # Check for special abilities
        has_special = context.get('has_special_ability', False)
        special_ready = context.get('special_ready', False)
        
        if self.strategy == "berserker":
            # Always attack
            return {
                "type": "attack",
                "description": f"{self.name} attacks recklessly!"
            }
        
        elif self.strategy == "basic":
            # Use special if available, otherwise attack
            if has_special and special_ready and random.random() < 0.5:
                return {
                    "type": "special",
                    "description": f"{self.name} uses a special ability!"
                }
            return {
                "type": "attack",
                "description": f"{self.name} attacks!"
            }
        
        elif self.strategy == "tactical":
            # Consider positioning and abilities
            in_good_position = context.get('has_advantage', False)
            
            if not in_good_position and random.random() < 0.3:
                return {
                    "type": "reposition",
                    "description": f"{self.name} moves to a better position!"
                }
            
            if has_special and special_ready and random.random() < 0.7:
                return {
                    "type": "special",
                    "description": f"{self.name} uses a tactical ability!"
                }
            
            return {
                "type": "attack",
                "description": f"{self.name} attacks strategically!"
            }
        
        else:  # mastermind
            # Complex decision tree
            hp_percent = (self.hit_points / self.max_hp) * 100
            
            # Low health? Use defensive ability or heal
            if hp_percent < 50 and context.get('has_heal', False):
                return {
                    "type": "heal",
                    "description": f"{self.name} uses a healing ability!"
                }
            
            # Buff allies if available
            if context.get('can_buff', False) and random.random() < 0.4:
                return {
                    "type": "buff",
                    "description": f"{self.name} empowers their allies!"
                }
            
            # Use special at optimal time
            if has_special and special_ready:
                num_targets = context.get('num_targets_in_range', 1)
                if num_targets >= 2:  # AOE opportunity
                    return {
                        "type": "special",
                        "description": f"{self.name} unleashes a devastating area attack!"
                    }
            
            # Coordinate with allies
            if context.get('ally_nearby', False) and random.random() < 0.5:
                return {
                    "type": "coordinate",
                    "description": f"{self.name} coordinates with allies for a flanking attack!"
                }
            
            return {
                "type": "attack",
                "description": f"{self.name} attacks with precision!"
            }
    
    def take_damage(self, damage: int):
        """Update HP and morale when taking damage"""
        self.hit_points = max(0, self.hit_points - damage)
        
        # Morale decreases with damage
        morale_loss = (damage / self.max_hp) * 50
        self.morale = max(0, self.morale - morale_loss)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "name": self.name,
            "hp": self.hit_points,
            "max_hp": self.max_hp,
            "hp_percent": (self.hit_points / self.max_hp) * 100,
            "morale": self.morale,
            "strategy": self.strategy,
            "intelligence": self.intelligence
        }


class CombatCoordinator:
    """Coordinates multiple enemies in combat"""
    
    def __init__(self):
        self.enemies: Dict[str, EnemyAI] = {}
        self.turn_order = []
    
    def add_enemy(self, name: str, intelligence: int, hp: int, max_hp: int):
        """Add an enemy to the combat"""
        self.enemies[name] = EnemyAI(name, intelligence, hp, max_hp)
        self.turn_order.append(name)
    
    def plan_round(self, players: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Plan actions for all enemies this round
        
        Returns:
            List of planned actions
        """
        actions = []
        
        for enemy_name in self.turn_order:
            if enemy_name not in self.enemies:
                continue
            
            enemy = self.enemies[enemy_name]
            
            if enemy.hit_points <= 0:
                continue
            
            # Choose target
            target = enemy.choose_target(players)
            
            # Choose action
            action = enemy.choose_action(context)
            action['enemy'] = enemy_name
            action['target'] = target.get('name') if target else None
            
            actions.append(action)
        
        return actions
    
    def get_all_status(self) -> List[Dict[str, Any]]:
        """Get status of all enemies"""
        return [enemy.get_status() for enemy in self.enemies.values()]


# Tool definition for strategic AI
def plan_enemy_actions(enemies: List[Dict], players: List[Dict], context: Dict = None) -> Dict[str, Any]:
    """
    Plan intelligent enemy actions for combat
    
    Args:
        enemies: List of enemy dicts with name, intelligence, hp, max_hp
        players: List of player dicts with name, health, threat_level
        context: Combat context
    
    Returns:
        Planned actions for each enemy
    """
    coordinator = CombatCoordinator()
    
    for enemy in enemies:
        coordinator.add_enemy(
            enemy['name'],
            enemy.get('intelligence', 10),
            enemy.get('hp', 50),
            enemy.get('max_hp', 50)
        )
    
    actions = coordinator.plan_round(players, context or {})
    
    return {
        "success": True,
        "actions": actions,
        "description": f"Planned {len(actions)} enemy actions using strategic AI"
    }


STRATEGIC_AI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "plan_enemy_actions",
            "description": "Use strategic AI to plan intelligent enemy actions in combat. Enemies will act based on their intelligence scores.",
            "parameters": {
                "type": "object",
                "properties": {
                    "enemies": {
                        "type": "array",
                        "description": "List of enemies with name, intelligence, hp, max_hp",
                        "items": {
                            "type": "object"
                        }
                    },
                    "players": {
                        "type": "array",
                        "description": "List of players with name, health, threat_level",
                        "items": {
                            "type": "object"
                        }
                    },
                    "context": {
                        "type": "object",
                        "description": "Combat context (terrain, special abilities available, etc.)"
                    }
                },
                "required": ["enemies", "players"]
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "plan_enemy_actions": plan_enemy_actions
}
