161.53.18.12,1955
ExperientialSamplingAnalyticsDev
roko
g546z6rhtf


downloadScript -> filter_size -> removeSlashes -> removeSlashes2 -> removeDoubleQuotes -> parsingScript


slide_switch
action_end
widget_log <<<<<<<<<<<
action_start
player_stop
player_start

PITANJA:
	(1) kako prepoznati krajnje logove (i pojedinačne)?
	(2) in contextualInfo-> userId je za identifikaciju
	(3) 'correct' i 'tocno' nebi trebao koristiti?
	
RAZMISLITI:
	(1) trebat će mi identifikator pitanja (težine su različite) -> string pitanja, kategorija pitanja (unknown)... (ovisi o broju podataka, da u jednoj grupi bude bar 100 pitanja)
	(2) kako rangirati studenta:
		(a) postoci iznad prosjeka (npr 10% bolji od prosjeka - kako se prosjek računa), težinski prosijek (prosijek, samo pitanja imaju drugaćiju težinu)

		
		
		
		
params["logDetails"].keys() i params["logDetails"][0].keys() 
'inputParams', 'logEntries', 'result'
'options', 'data', 'type'
'gameLog', 'time'
'group', 'data', 'iframeId', 'type'
'data', 'type'

params?['inputParams'].keys() = 'isAdaptive', 'groupMembers', 'brojPonavljanja', 'isCollaborative', 'lekcija', 'tezina', 'naslov'
logEntries!!!
params?['result'].keys()= 'score', 'duration'

Options -> None
data ->
dict_keys(['rbr', 'firstPart', 'secondPart', 'thirdPart', 'checkCurrentSolution', 'group'])
dict_keys(['inputParams', 'partial_logEntries'])
dict_keys(['rbr', 'firstPart', 'secondPart', 'thirdPart', 'fourthPart', 'group'])
dict_keys(['rbr', 'currentSolution', 'checkCurrentSolution', 'group'])
dict_keys(['type', 'authorElapsedTime'])
dict_keys(['type', 'authorElapsedTime', 'editorElapsedTime'])
dict_keys(['rbr', 'currentSolution', 'firstPart', 'secondPart', 'thirdPart', 'fourthPart', 'group'])
dict_keys(['type', 'discuss'])
dict_keys(['type'])
dict_keys(['type', 'correct'])
dict_keys(['type', 'editorElapsedTime'])
dict_keys(['rbr', 'firstPart', 'secondPart', 'thirdPart', 'fourthPart', 'checkCurrentSolution', 'group'])
dict_keys(['rbr', 'currentSolution', 'group'])
dict_keys(['type', 'button'])
dict_keys([])
type -> 
widget_partial_log
update-state
get-state-from-backend
post-group-message
ready

gamelog !!!!!!!!!!!!!





dependencies:
	tensorflow
	pymssql