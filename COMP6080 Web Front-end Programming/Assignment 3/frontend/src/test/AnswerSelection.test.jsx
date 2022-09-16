import React from 'react';
import { shallow } from 'enzyme';

// MUI components
import { Button } from '@mui/material';

// own component
import AnswerSelection from '../components/AnswerSelection';

describe('<AnswerSelection />', () => {
  let wrapper;
  const answer = { answerContext: 'Answer_1', correct: false };

  it('renders without crashing', () => {
    wrapper = shallow(<AnswerSelection answer={answer} />);
  })

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('should have text', () => {
    expect(wrapper.find('.answerText').text()).toBe('Answer_1');
  })

  it('should render one component', () => {
    expect(wrapper.find(Button)).toHaveLength(1);
  })
})
