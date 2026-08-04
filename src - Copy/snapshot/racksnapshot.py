"""
racksnapshot.py — VMS 3000  •  Module Snapshot Configuration
Defines module display configurations for rack slots.
"""

# Module type definitions
MODULE_TYPES = {
    "3000/6M": {
        "name": "VMM-6M",
        "type": "proximeter",
        "display": "image",
        "components": {
            "logo": {
                "type": "oval",
                "color": "#1a5fa0",
                "border": "#4a9fd0"
            },
            "indicators_top": [
                {"label": "PWR", "color": "#00ff00"},
                {"label": "Tx/Rx", "color": "#888888"},
                {"label": "OK", "color": "#888888"}
            ],
            "alarm_section": {
                "label": "ALARM",
                "indicators": [
                    {"label": "OK", "color": "#888888"},
                    {"label": "ALT", "color": "#888888"},
                    {"label": "DAN", "color": "#888888"},
                    {"label": "BYP", "color": "#888888"}
                ]
            },
            "connectors": {
                "type": "BNC",
                "count": 4,
                "color": "#c0c0c0"
            },
            "label": "VMM-6M"
        }
    },
    "3000/12M/DIS": {
        "name": "VMM-12M/DIS",
        "type": "proximeter",
        "display": "standard"
    },
    "3000/12M/TAC": {
        "name": "VMM-12M/TAC",
        "type": "tachometer",
        "display": "standard"
    },
    "3000/6M/TAC": {
        "name": "VMM-6M/TAC",
        "type": "tachometer",
        "display": "standard"
    }
}

# Slot configuration mapping
SLOT_CONFIG = {
    # When a slot contains "3000/6M", it will display the detailed image
    "3000/6M": MODULE_TYPES["3000/6M"]
}


def get_module_config(module_name: str) -> dict:
    """
    Get module configuration by name.
    
    Args:
        module_name: Name of the module (e.g., "3000/6M")
    
    Returns:
        Dictionary containing module configuration
    """
    return MODULE_TYPES.get(module_name, {})


def is_image_display_module(module_name: str) -> bool:
    """
    Check if a module should be displayed as an image.
    
    Args:
        module_name: Name of the module
    
    Returns:
        True if module should display as image, False otherwise
    """
    config = MODULE_TYPES.get(module_name, {})
    return config.get("display") == "image"
