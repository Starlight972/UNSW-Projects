import React from 'react';
import { shallow } from 'enzyme';
import { CopyToClipboard } from 'react-copy-to-clipboard';

// MUI components
import Button from '@mui/material/Button';

// own component
import SessionId from '../components/SessionId';

describe('<SessionId />', () => {
  let wrapper;
  const sessionId = 1234;

  it('renders without crashing', () => {
    wrapper = shallow(<SessionId sessionId={sessionId} />);
  })

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('should have text', () => {
    expect(wrapper.find('#session').text()).toBe('Session ID: 1234');
  })

  it('should render one component', () => {
    expect(wrapper.find(Button)).toHaveLength(1);
    expect(wrapper.find(CopyToClipboard)).toHaveLength(1);
  })
})
