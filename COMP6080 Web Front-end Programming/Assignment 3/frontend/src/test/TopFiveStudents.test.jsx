import React from 'react';
import { shallow } from 'enzyme';
import '@testing-library/jest-dom/extend-expect';
import { render, screen } from '@testing-library/react';

// own component
import TopFiveStudents from '../components/TopFiveStudents';

describe('<TopFiveStudents />', () => {
  let wrapper;

  it('renders without crashing', () => {
    wrapper = shallow(<TopFiveStudents />);
  })

  it('matches snapshot', () => {
    expect(wrapper).toMatchSnapshot();
  });
});

test('renders text elements', () => {
  render(<TopFiveStudents questions={[]} results={[]} />);
  const text = screen.getByText('Top 5');
  expect(text).toBeInTheDocument();
});
