# if you want to add more events, do so in the following format:
#'Name': (startframe, endframe, "minlon/maxlon/minlat/maxlat", "projection", vectorscale, "occurance time (historical)", "magnitude (historical)")}
#make sure to keep mod_pars formated as a dictionary, inside brackets
mod_pars = {'Tohoku': (341, 541, "133/151/30/46", "M7i", 1.6, "14:46", "9.1"),
'Mentawai': (330, 600, "70/140/-20/25", "M16i", 150, "21:42", "7.7"),
'San Andreas': (20, 60, "-125/-115/32/42", "M16i", 80, "fake", "fake"),
'Hayward': (20, 60, "-125/-115/32/42", "M16i", 80, "fake", "fake"),
'Elsinore': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'Maacama': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'Newport-Inglewood-Rose Canyon': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'Zayante-Vergeles': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'San Jacinto': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'Calaveras': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'West Napa': (60, 100, "-125/-115/32/42", "M16i", 20, "fake", "fake"),
'Cascadia': (279, 411, "233/238/46/50", "M7i", 5, "", "7.6")}


def get_mod_pars(mod, mod_pars=mod_pars):
	return(mod_pars[mod][0], mod_pars[mod][1], mod_pars[mod][2], mod_pars[mod][3], mod_pars[mod][4], mod_pars[mod][5], mod_pars[mod][6])
