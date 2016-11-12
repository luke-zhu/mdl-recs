import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

const Shows = new Mongo.Collection('Shows');

Meteor.methods({
  'shows.getTop': (numShows) => {
    check(numShows, Number);
    return (
      Shows.find({ 'avg(rating)': { $gt: 8.5 } }, {
        sort: { count: -1 },
        limit: numShows,
      }).fetch()
    );
  },
});

export default Shows;
