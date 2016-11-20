import React, { PropTypes, Component } from 'react';
import Chart from 'chart.js';
import { Meteor } from 'meteor/meteor';
import { connect } from 'react-redux';
import Paper from 'material-ui/Paper';

import { getTopShows } from '../redux/actions';

class MDLTopShows extends Component {
  componentDidMount() {
    this.props.updateShows();
  }
  componentDidUpdate() {
    this.renderChart();
  }
  renderChart() {
    this.chart_instance = new Chart(this.node, {
      type: 'bar',
      data: {
        labels: this.props.shows.map(show => show.title),
        datasets: [{
          label: '# of Ratings',
          data: this.props.shows.map(show => show.num_scores),
          backgroundColor: 'rgba(132, 255, 99, 0.2)',
          borderColor: 'rgba(132, 255, 99, 1)',
          borderWidth: 1,
        }],
      },
      options: {
        title: {
          display: true,
          position: 'bottom',
          text: 'Most watched shows rated at least 8.5 by recent forum users',
        },
        scales: {
          xAxes: [{
            display: false,
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
            },
          }],
        },
      },
    });
  }
  render() {
    return (
      <Paper style={{ padding: 10, marginBottom: 20 }} zDepth={2}>
        <h2>Statistics</h2>
        <canvas
          ref={node => this.node = node}
        />
      </Paper>
    );
  }
}

MDLTopShows.propTypes = {
  updateShows: PropTypes.func.isRequired,
  shows: PropTypes.array.isRequired,
};

const mapStateToProps = state => ({
  shows: state.topShows,
});

const mapDispatchToProps = dispatch => ({
  updateShows: () => {
    Meteor.call('shows.getTop', 20, (error, result) => {
      if (error) console.error(error);
      else {
        dispatch(getTopShows(result));
      }
    });
  },
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(MDLTopShows);
