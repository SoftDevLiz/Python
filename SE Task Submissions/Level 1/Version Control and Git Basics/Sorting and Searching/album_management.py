class Album:
    def __init__(self, album_name, number_of_songs, album_artist):
        self.album_name = album_name
        self.number_of_songs = number_of_songs
        self.album_artist = album_artist

    def __str__(self):
        return (
            f"{self.album_name} by {self.album_artist}"
            f" ({self.number_of_songs} songs)"
        )


hybrid_theory = Album("Hybrid Theory", 12, "Linkin Park")
meteora = Album("Meteora", 13, "Linkin Park")
minutes_to_midnight = Album("Minutes to Midnight", 12, "Linkin Park")
a_thousand_suns = Album("A Thousand Suns", 15, "Linkin Park")
living_things = Album("Living Things", 12, "Linkin Park")


albums1 = [hybrid_theory, meteora, minutes_to_midnight,
           a_thousand_suns, living_things]

print("\n")

for album in albums1:
    print(f"Albums1: {album}")

print("\n")

albums1.sort(key=lambda album: album.number_of_songs)

for album in albums1:
    print(f"Albums1 sorted by songs: {album}")

print("\n")

albums1[0], albums1[1] = albums1[1], albums1[0]

for album in albums1:
    print(f"Albums1 index 0 and 1 swapped: {album}")

print("\n")

wet_leg_self_titled = Album("Wet Leg", 12, "Wet Leg")
moisturizer = Album("Moisturizer", 12, "Wet Leg")
apple_music_home = Album("Apple Music Home Session", 2, "Wet Leg")
spotify_singles = Album("Spotify Singles", 2, "Wet Leg")
chaise_longue_ep = Album("Chaise Longue (EP)", 2, "Wet Leg")

albums2 = [wet_leg_self_titled, moisturizer,
           apple_music_home, spotify_singles, chaise_longue_ep]

for album in albums2:
    print(f"Albums2; {album}")

print("\n")

for album in albums1:
    albums2.append(album)

dark_side_of_the_moon = Album("Dark Side of The Moon", 9, "Pink Floyd")
oops_i_did_it_again = Album("Oops!...I Did It Again", 16, "Britney Spears")

albums2.append(dark_side_of_the_moon)
albums2.append(oops_i_did_it_again)

albums2.sort(key=lambda album: album.album_name)

for album in albums2:
    print(f"Albums2 updated: {album}")

index = None

for i, album in enumerate(albums2):
    if album.album_name == "Dark Side of The Moon":
        index = i
        break

print("\n")

print(f"Index of 'Dark Side of The Moon': {index}")
