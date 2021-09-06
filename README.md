# ScratchTracker

I was approached by a client who asked me to build them an application that allows them to track their medical intake of eczema medication, as well as use a points system to see if they are having a particularly bad day. On the surface this seems like a relatively simple application to develop, however there were many unexpected issues that I had to overcome.

One of these issues was that the client wanted to have a button on the main screen of the app that allows them to check the current averages for medicines taken, as well as number of scratches in a week. This was an issue because the averages may change depending on the time of day they were checked. As django only renders in the data once, the averages would only be calculated based on the time the view was rendered. This is fine if the user refreshes the page before checking the averages, but that is not a good user experience.

The way i solved this issue was to use django rest to create an api with a get request that calculates the averages. I then used javascript to fetch the api each time the button was pressed. this meant that the data could be recalculated and re displayed, without the user having to refresh the page.

Another challenge with the application was the points system the client uses for their medication. some medications split their points over a span of 5 days, meaning if the medication had a total of 10 points, that would be 2 points for the next 5 days. This became a challenge when calculating the previous months averages. If they chose a medication on the second to last day of the previous month, the total points would span across 2 different months. I was able to use my mathematical skills to separate and distribute the points correctly.
