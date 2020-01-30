module.exports = (eventsHTML, groupsHTML) => `
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>CompiledEDI Events (Edinburgh Tech Meetups)</title>
    <link rel="stylesheet" href="style.css">
    <meta name="author" content="Sean O'Mahoney"/>
    <meta name="description" content="CompiledEDI Events (Edinburgh Tech Meetups) - Helping you find technology events through the use of Meetup and Eventbrite."/>
    <meta name="keywords" content="Edinburgh, Events, Tech, Technology, Networking, Meetup, Eventbrite, CompiledEDI"/>
</head>

<body>
    <header>
        <h1>CompiledEDI Events</h1>
        <p>Provided by <a href='https://creativeinformatics.org/' rel="noreferrer" target="_blank">Creative Informatics</a>. Based the <a href='https://events.compiledmcr.com/' rel="noreferrer" target="_blank">compiledMCR site</a> by Sean O'Mahoney.</p>
    </header>
    <summary>
        <p>Helping you find technology events through the use of Meetup and Eventbrite.</p>
    </summary>
    <main>
        <div id="typeContainer">
            <div id="selected" class="type">
                <p>Events</p>
            </div>
            <div class="type">
                <p>Groups</p>
            </div>
        </div>
        <div id="itemsContainer">
            <div id="eventContainer" class="itemsContainer">
                <div class="searchDiv">
                    <div id="eventsTopLevel">
                        <input type="button" id="eventsSorts" value="Sorts">
                        <input type="button" id="eventsFilters" value="Filters">
                        <input type="text" id="eventsSearchBox" class="search" value="">
                        <input type="button" id="eventsClearSearch" value="Clear">
                    </div>
                    <!-- <div id="eventsMiddleLevel">
                        <input type="button" id="eventsSourceType" value="Source">
                    </div>
                    <div id="eventsLowLevel">
                        <input type="button" id="eventsSourceEventbrite" value="Eventbrite">
                    </div> -->
                </div>
                <!-- <nav id="eventsNav" class="itemsNav">
                    <div id="eventsSearchBar">Search</div>
                    <div id="eventsReduceBar">Reduce</div>
                    <div id="eventsSpecificBar">Specific</div>
                </nav> -->
                <section id="eventsItems">
                    ${eventsHTML}
                </section>
            </div>
            <div id="groupContainer" class="itemsContainer" style="display:none;">
                <div class="searchDiv">
                    <input type="button" id="groupsSorts" value="Sorts">
                    <input type="button" id="groupFilters" value="Filters">
                    <input type="text" id="groupsSearchBox" class="search" value="">
                    <input type="button" id="groupsClearSearch" value="Clear">
                </div>
                <!-- <nav id="groupsNav" class="itemsNav">
                    <div id="groupsSearchBar">Search</div>
                    <div id="groupsReduceBar">Reduce</div>
                    <div id="groupsSpecificBar">Specific</div>
                </nav> -->
                <section id="groupsItems">
                    ${groupsHTML}
                </section>
            </div>
        </div>
    </main>
    <footer>Find me on <a href="https://github.com/Edinburgh-College-of-Art/compiled-edi-events" target="_blank" rel="noreferrer"><p>GitHub</p></a></footer>
    <div id="toTop"><img src="./img/chevron-arrow-up.svg" width="15px"></div>
    <script src="./scripts/dataToHTML.js"></script>
    <script src="./scripts/main.js"></script>

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-111660061-2"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-111660061-2');
    </script>

</body>

</html>
`
