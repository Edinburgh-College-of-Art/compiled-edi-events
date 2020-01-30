let meetup = require("./sources/meetup"),
    eventbrite = require("./sources/eventbrite"),
    googleCalendar = require("./sources/googleCalendar"),
    googleCalendarKey = "AIzaSyCR3-ptjHE-_douJsn8o20oRwkxt-zHStY"; // Calendar API Key gained from the Google Developer Console, this key is shown in many examples

class dataGather {
    constructor() {
        this.eventbrite = new eventbrite();
        this.meetup = new meetup();
        this.googleCalendar = new googleCalendar("a73q3trj8bssqjifgolb1q8fr4@group.calendar.google.com", "https://technw.uk/calendar", "TechNW", googleCalendarKey);
        // this.sources = [this.eventbrite, this.meetup, this.googleCalendar];
        this.sources = [this.eventbrite, this.meetup];
    }

    async getData() {
        return new Promise(resolve => {
            Promise.all(this.sources.map(api => api.getData())).then(data => {
                console.table(data)
                // Joining data from all sources
                let groupsData = data.reduce((total, curr) => total.concat(curr[0]), []);
                let eventsData = data.reduce((total, curr) => total.concat(curr[1]), []);
                // Sorting / Filtering
                let groups = this.sortNames(groupsData);
                let events = this.sortTime(this.filterEvents(eventsData));
                resolve([groups, events]);
            })
        });
    }

    sortTime(items) {
        return items.sort((a, b) => new Date(a.startTimeISO) - new Date(b.startTimeISO));
    }

    sortNames(items) {
        return items.sort((a, b) => {
            if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
            if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
            return 0;
        });
    }

    // https://stackoverflow.com/questions/2218999/remove-duplicates-from-an-array-of-objects-in-javascript
    filterEvents(events) {
        return events.filter((event,index) => {
            return index === events.findIndex(obj => {
              return this.rtnLowercaseAlpha(event.name) == this.rtnLowercaseAlpha(obj.name) && this.formatDate(event.startTimeISO) == this.formatDate(obj.startTimeISO);
            });
          });
    }

    rtnLowercaseAlpha(string) {
        return string.toLowerCase().replace(/[^a-z0-9]/gi,'');
    }

    // https://stackoverflow.com/questions/23593052/format-javascript-date-to-yyyy-mm-dd
    formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [day, month, year].join('-');
    }
}

module.exports = dataGather;
