"""
Character Parser - Extracts character updates from player actions
"""
import re

def parse_character_updates(action: str, character):
    """
    Parse player action and update character accordingly.
    Returns True if character was modified, False otherwise.
    """
    action_lower = action.lower()
    modified = False
    
    print(f"[PARSER] Parsing action: {action}")
    
    # Class changes - more flexible detection
    class_keywords = {
        'wizard': 'Wizard',
        'mage': 'Wizard',
        'fighter': 'Fighter',
        'warrior': 'Fighter',
        'rogue': 'Rogue',
        'thief': 'Rogue',
        'cleric': 'Cleric',
        'priest': 'Cleric',
        'paladin': 'Paladin',
        'ranger': 'Ranger',
        'barbarian': 'Barbarian',
        'bard': 'Bard',
        'druid': 'Druid',
        'monk': 'Monk',
        'sorcerer': 'Sorcerer',
        'warlock': 'Warlock'
    }
    
    # Check for class change with multiple patterns
    class_change_patterns = [
        r'change\s+(?:my\s+)?class\s+to\s+(\w+)',
        r'become\s+(?:a\s+)?(\w+)',
        r'switch\s+to\s+(\w+)',
        r'(?:i\s+am\s+now\s+a\s+|i\s+am\s+a\s+)(\w+)',
    ]
    
    for pattern in class_change_patterns:
        match = re.search(pattern, action_lower)
        if match:
            class_word = match.group(1).lower()
            if class_word in class_keywords:
                class_name = class_keywords[class_word]
                character.character_class = class_name
                modified = True
                # Adjust stats based on class
                if class_name == 'Wizard':
                    character.intelligence = 16
                    character.strength = 8
                    character.dexterity = 10
                    character.charisma = 12
                elif class_name == 'Sorcerer':
                    character.charisma = 16
                    character.intelligence = 14
                    character.strength = 8
                    character.dexterity = 10
                elif class_name == 'Fighter':
                    character.strength = 16
                    character.constitution = 14
                    character.intelligence = 8
                    character.dexterity = 12
                elif class_name == 'Rogue':
                    character.dexterity = 16
                    character.charisma = 14
                    character.strength = 10
                    character.intelligence = 12
                elif class_name == 'Cleric':
                    character.wisdom = 16
                    character.constitution = 14
                    character.strength = 12
                    character.intelligence = 10
                elif class_name == 'Paladin':
                    character.strength = 15
                    character.charisma = 14
                    character.constitution = 14
                    character.wisdom = 12
                elif class_name == 'Ranger':
                    character.dexterity = 15
                    character.wisdom = 14
                    character.constitution = 13
                    character.strength = 12
                elif class_name == 'Barbarian':
                    character.strength = 17
                    character.constitution = 16
                    character.dexterity = 12
                    character.intelligence = 8
                elif class_name == 'Bard':
                    character.charisma = 16
                    character.dexterity = 14
                    character.intelligence = 12
                    character.wisdom = 10
                elif class_name == 'Druid':
                    character.wisdom = 16
                    character.constitution = 14
                    character.intelligence = 12
                    character.strength = 10
                elif class_name == 'Monk':
                    character.dexterity = 16
                    character.wisdom = 15
                    character.constitution = 13
                    character.strength = 12
                elif class_name == 'Warlock':
                    character.charisma = 16
                    character.constitution = 14
                    character.intelligence = 12
                    character.dexterity = 10
                break  # Only match first class change pattern
    
    if modified:
        print(f"[PARSER] Character updated: Class={character.character_class}, STR={character.strength}, DEX={character.dexterity}, CON={character.constitution}, INT={character.intelligence}, WIS={character.wisdom}, CHA={character.charisma}")
    
    # Level up
    if 'level up' in action_lower or 'gain level' in action_lower:
        character.level += 1
        character.max_health += 10
        character.health = character.max_health
        modified = True
    
    # Add items to inventory - improved patterns
    item_patterns = [
        r'add\s+(?:a\s+|an\s+|the\s+)?(.+?)\s+to\s+(?:my\s+)?inventory',
        r'(?:pick up|take|grab|get|loot|find)\s+(?:a\s+|an\s+|the\s+)?(.+)',
    ]
    
    for pattern in item_patterns:
        match = re.search(pattern, action_lower)
        if match:
            item = match.group(1).strip()
            # Clean up common words
            item = item.replace(' to inventory', '').replace(' to my inventory', '')
            if item and len(item) < 50:  # Reasonable item name length
                character.inventory.append(item)
                modified = True
                break
    
    return modified
