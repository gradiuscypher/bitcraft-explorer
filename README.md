# Bitcraft Explorer

## Ideas

### TUI Ideas
- TUI interface with different tables on the left that allow you to subscribe to messages
- Messages appear in the center
- Can write plugins that process the messages and do other things with them?

### Project Ideas
- Parse chat and create requests if someone wants something
    - eg: someone says Leatherworking 40 LWF places them in a queue that allows other people to use discord to request their help? or maybe a website that displays requests/LFW

## Research Notes
- `passive_craft_state` can be queried by owner_id to get all passive crafts running for that user
- `admin_broadcast` might be an interesting discord bot idea
- `dropped_inventory_state` - you can see everything dropped on the ground
- `exploration_chunks_state` - might be fun to track how fast its growing
- `extract_outcome_state` - when a player is gathering, maybe alert if havent gathered in a while?
- `growth_state` - track plant growth?
- `player_state` - hours played
- `traveler_task_state` - help people finish their tasks