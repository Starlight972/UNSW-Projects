import React from 'react';
import { shallow } from 'enzyme';
import '@testing-library/jest-dom/extend-expect';

// MUI components
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

// own component
import TimeSelector from '../components/TimeSelector';

describe('<TimeSelector />', () => {
  const noop = () => {};

  it('renders without crashing', () => {
    const component = shallow(<TimeSelector setTime={noop} />);
    console.log(component);
  })

  it('matches snapshot', () => {
    const component = shallow(<TimeSelector setTime={noop} />);
    expect(component).toMatchSnapshot();
  });

  it('should has elements correct', () => {
    const component = shallow(<TimeSelector setTime={noop} />);
    expect(component.find(InputLabel)).toHaveLength(1);
    expect(component.find(InputLabel).text()).toEqual('Time Limit');
    expect(component.find(FormControl)).toHaveLength(1);
    expect(component.find(Select)).toHaveLength(1);
    expect(component.find(MenuItem)).toHaveLength(8);
  })

  it('uses fallback time if none provided', () => {
    const component = shallow(<TimeSelector setTime={noop} />);
    expect(component.find(Select).props().value).toBe(undefined);
  })

  it('uses fallback time if provided', () => {
    const component = shallow(<TimeSelector setTime={noop} time={5} />);
    expect(component.find(Select).props().value).toBe(5);
  })

  it('triggers onChange event handler when clicked', () => {
    const onChange = jest.fn();
    const component = shallow(<TimeSelector setTime={onChange} />);
    const select = component.find(Select);
    select.simulate('change', { target: { value: 5 } });
    expect(onChange).toHaveBeenCalledTimes(1);
  })
})
