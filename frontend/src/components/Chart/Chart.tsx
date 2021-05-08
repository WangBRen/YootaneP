import React ,{Component} from 'react';
import { Card } from 'antd'
import ReactEcharts from 'echarts-for-react';
class Bar extends Component{
    constructor(props){
        super(props)
        this.state = {
            rate:[50, 50],
            // stores:[15, 120, 36, 110, 110, 20]
        }
    }
    /**
     * 生成概率统计图的组件
     */
    getOption = (rate) =>{
        return {
            title: {
                text: 'ECharts'
            },
            tooltip: {},
            legend: {
                data:['概率']
            },
            xAxis: {
                data: ["1","0"]
            },
            yAxis: {},
            series: [{
                name: '概率',
                type: 'bar',
                data: rate
            }]
        };
    }
    render(){
        const { rate } = this.state;
        return(
            <div>
                <Card>
                    <ReactEcharts option={this.getOption(rate)} />
                </Card>
            </div>
        )
    }
}
export default Bar;