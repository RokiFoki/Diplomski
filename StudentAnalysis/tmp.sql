SELECT 
	[User].Name, 
	LogEvent.Id, 
	LogEvent.EventName, 
	LogEvent.EventType, 
	LogEvent.Time, 
	CONVERT(NVARCHAR(MAX), LogEvent.JSONparams), 
	LogEvent.ContextualInfoId 
FROM 
	LogEvent
JOIN 
	ContextualInfo ON LogEvent.ContextualInfoId = ContextualInfo.Id
JOIN 
	[User] ON ContextualInfo.UserId = [User].Id
WHERE 
	JSONparams LIKE '%{%}%' AND LogEvent.EventType = 'Player'
	eventName = 'widget_log' AND 
	(
		(ContextualInfo.Time BETWEEN '3/25/2016' and '3/25/2016 23:59:59') OR
		(ContextualInfo.Time BETWEEN '3/26/2016' and '3/26/2016 23:59:59') OR
		(ContextualInfo.Time BETWEEN '3/29/2016' and '3/29/2016 23:59:59') OR
		(ContextualInfo.Time BETWEEN '3/30/2016' and '3/30/2016 23:59:59') OR
		(ContextualInfo.Time BETWEEN '3/31/2016' and '3/31/2016 23:59:59') OR
		(ContextualInfo.Time BETWEEN '4/1/2016' and '4/1/2016 23:59:59') 
    )
        