import React from 'react';
import { Button } from 'antd';
import 'antd/lib/button/style'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import IpService from '../service/Ip';

const service = new IpService()

export default class Getip extends React.Component {
    render () {
        return <_Getip service={service}/>
    }
}

class _Getip extends React.Component {
    handleClick(event) {
        this.props.service.getip()
        console.log('hhhhh')
    }


    render() {
        return (
            <div>
                <Button onClick={this.handleClick.bind(this)}>获取IP池</Button>
            </div>
        )
    }
}