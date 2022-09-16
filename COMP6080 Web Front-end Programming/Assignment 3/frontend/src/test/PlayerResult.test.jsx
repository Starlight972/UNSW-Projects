import React from 'react';
import { shallow } from 'enzyme';
import '@testing-library/jest-dom/extend-expect';
import { render, screen } from '@testing-library/react';

// MUI components
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';

// own component
import PlayerResult from '../components/PlayerResult';

describe('<PlayerResult />', () => {
  it('renders without crashing', () => {
    const component = shallow(<PlayerResult />);
    console.log(component);
  })

  it('matches snapshot', () => {
    const component = shallow(<PlayerResult />);
    expect(component).toMatchSnapshot();
  });

  it('should has none elements correct if none provided', () => {
    const component = shallow(<PlayerResult />);
    expect(component.find(CheckIcon)).toHaveLength(0);
    expect(component.find(ClearIcon)).toHaveLength(1);
  })

  it('should has elements correct if correct check provided', () => {
    const component = shallow(<PlayerResult isCorrect={true} />);
    expect(component.find(CheckIcon)).toHaveLength(1);
    expect(component.find(ClearIcon)).toHaveLength(0);
  })

  it('uses fallback number if provided', () => {
    render(<PlayerResult num={1} />);
    const title = screen.getByText('Question 1')
    expect(title).toBeInTheDocument();
  })
})
