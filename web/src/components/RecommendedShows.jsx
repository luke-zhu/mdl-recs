import React, {Component} from 'react';
import PropTypes from 'prop-types';

import Chart from 'chart.js';
import Paper from 'material-ui/Paper';

class RecommendedShows extends Component {
    componentDidMount() {
        this.renderChart();
    }

    renderChart() {
        this.chart_instance = new Chart(this.node, {
            type: 'bar',
            data: {
                labels: this.props.similarShows.map(show => show._id),
                datasets: [{
                    label: 'Similarity',
                    data: this.props.similarShows.map(show => show.averageSimilarity),
                    backgroundColor: 'rgba(132, 255, 99, 0.2)',
                    borderColor: 'rgba(132, 255, 99, 1)',
                    borderWidth: 1,
                }],
            },
            options: {
                title: {
                    display: true,
                    position: 'bottom',
                    text: 'Shows similar to those you have completed',
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
        // console.log(this.props.myShows);
        // console.log(this.props.similarShows);
        return (
            <Paper style={{padding: 10, marginBottom: 20}} zDepth={2}>
                <h2>Recommended Shows</h2>
                <canvas
                    ref={node => this.node = node}
                />
            </Paper>
        );
    }
}

RecommendedShows.propTypes = {
    myShows: PropTypes.array.isRequired,
    similarShows: PropTypes.array.isRequired,
};

export default RecommendedShows;
