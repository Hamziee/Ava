# Source file for music command strings.
# File version: v2.0
# - x.0 → Increment x by 1 if new string(s) are added or removed.
# - 0.x → Increment x by 1 if existing string(s) are changed or removed.
# A language needs translation if the language version doesn't match this version. This file (en_US.py) is always the source file for any translation.

# Error messages
error = "Error"
must_be_in_voice = "You must be in a voice channel!"
already_in_another_voice = "I'm already in another voice channel."
no_music_playing = "No music or radio is currently playing."
queue_empty = "The queue is empty."
invalid_page = "Invalid page. Please select a page between 1 and {max_pages}."
not_in_voice = "I'm not in a voice channel."
no_results = "Could not find any results for your query."
processing_error = "An error occurred while processing the song: {error}"
invalid_song_data = "Found results but couldn't extract valid song data."
radio_not_found = "Radio station not found."

# Success messages
searching = "Searching..."
searching_for = "Searching for `{query}`..."
song_added = "Song Added"
song_info = "[**{title}**]({url}) by **{author}**\nRequested by **{requester}** | Duration: {duration} seconds"
skipped = "Skipped"
skipped_success = "Skipped the current song."
disconnected = "Disconnected"
disconnect_success = "Left the voice channel and cleared the queue."

# Now playing
now_playing = "Now Playing"
queue_title = "Queue"
queue_page = "**Page {page}/{max_pages}**\n\n{queue_str}"

# Radio
radio_title = "Radio Station"
radio_playing = "Now playing {name} - {description}"
radio_switched = "Switched to radio mode"
radio_stopped = "Radio stopped"

# Footer
version = "version"
by = "by"
footer_extra = "Music & Radio"