import React, { PropTypes, Component } from 'react';
import Chart from 'chart.js';
import { Meteor } from 'meteor/meteor';
import { connect } from 'react-redux';

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
        labels: this.props.shows.map(show => show.name),
        datasets: [{
          label: '# of Scores',
          data: this.props.shows.map(show => show['count']),
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
          ],
          borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
          ],
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
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
    console.log(this.props.shows);
    return (
      <div style={{ maxWidth: '800px', maxHeight: '500px' }}>
        <canvas
          ref={node => this.node = node}
          height="400"
          width="400"
        />
      </div>
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
    Meteor.call('shows.getTop', 10, (error, result) => {
      if (error) console.error(error);
      else dispatch(getTopShows(result));
    });
  },
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(MDLTopShows);
