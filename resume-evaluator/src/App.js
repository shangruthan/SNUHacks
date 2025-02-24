import React, { useState, useEffect } from 'react';
import styled, { ThemeProvider, createGlobalStyle, keyframes } from 'styled-components';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FaUser, FaBuilding, FaMoon, FaSun, FaInfoCircle } from 'react-icons/fa';

const lightTheme = {
  background: "#f8f9fa",
  text: "#333",
  cardBackground: "rgba(255, 255, 255, 0.3)",
  buttonBackground: "#007bff",
  buttonHover: "#0056b3",
  infoBackground: "rgba(255, 255, 255, 0.8)"
};

const darkTheme = {
  background: "#121212",
  text: "#f8f9fa",
  cardBackground: "rgba(30, 30, 30, 0.6)",
  buttonBackground: "#6610f2",
  buttonHover: "#520dc2",
  infoBackground: "rgba(30, 30, 30, 0.8)"
};

const fadeIn = keyframes`
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
`;

const slideIn = keyframes`
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${(props) => props.theme.background};
    color: ${(props) => props.theme.text};
    font-family: 'Arial', sans-serif;
    transition: all 0.3s ease;
  }
`;

const LoginPage = () => {
  const [userType, setUserType] = useState('');
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState(lightTheme);
  const [showInfo, setShowInfo] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setTheme(savedTheme === 'light' ? lightTheme : darkTheme);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === lightTheme ? darkTheme : lightTheme;
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme === lightTheme ? 'light' : 'dark');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userType) {
      toast.error('Please select a user type!');
      return;
    }
    setLoading(true);
    try {
      await axios.post('/api/login', { userType });
      toast.success('Login Successful! Redirecting...');
      setTimeout(() => {
        window.location.href = userType === 'individual' ? '/individual_dashboard' : '/company_dashboard';
      }, 1500);
    } catch {
      toast.error('Login Failed. Please try again.');
    }
    setLoading(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <ToastContainer position="top-right" autoClose={2000} />
      <PageContainer>
        <HeroBackground>
          <Card>
            <h1>Resume Evaluator</h1>
            <Subtitle>Empowering Careers, Enhancing Hiring</Subtitle>
            <Form onSubmit={handleSubmit}>
              <Label>
                <input type="radio" name="user_type" value="individual" checked={userType === 'individual'} onChange={() => setUserType('individual')} />
                <FaUser /> Individual (Resume Enhancement)
              </Label>
              <Label>
                <input type="radio" name="user_type" value="company" checked={userType === 'company'} onChange={() => setUserType('company')} />
                <FaBuilding /> Company (Resume Evaluation)
              </Label>
              <AnimatedButton type="submit" disabled={loading}>
                {loading ? 'Processing...' : 'Proceed to Login'}
              </AnimatedButton>
            </Form>
            <ThemeToggle onClick={toggleTheme}>
              {theme === lightTheme ? <FaMoon /> : <FaSun />}
            </ThemeToggle>
            <InfoToggle onClick={() => setShowInfo(!showInfo)}>
              <FaInfoCircle /> {showInfo ? 'Hide Info' : 'Why Choose Us?'}
            </InfoToggle>
          </Card>
        </HeroBackground>
        {showInfo && (
          <InfoSection>
            <h2>Why Choose Our Resume Evaluator?</h2>
            <FeatureList>
              <FeatureItem>
                <strong>AI-Powered Analysis:</strong> Our advanced algorithms provide in-depth resume insights[12].
              </FeatureItem>
              <FeatureItem>
                <strong>ATS Optimization:</strong> Ensure your resume passes through Applicant Tracking Systems[16].
              </FeatureItem>
              <FeatureItem>
                <strong>Customized Feedback:</strong> Receive tailored suggestions to enhance your resume[14].
              </FeatureItem>
              <FeatureItem>
                <strong>Industry-Specific Insights:</strong> Get recommendations based on your target industry[18].
              </FeatureItem>
            </FeatureList>
          </InfoSection>
        )}
        <Footer>
          <p>&copy; 2025 Resume Evaluator. All rights reserved.</p>
        </Footer>
      </PageContainer>
    </ThemeProvider>
  );
};

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
`;

const HeroBackground = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('https://source.unsplash.com/1600x900/?technology,abstract') center/cover no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: -1;
`;

const Card = styled.div`
  background: ${(props) => props.theme.cardBackground};
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 350px;
  color: ${(props) => props.theme.text};
  animation: ${fadeIn} 0.5s ease-out;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  }
`;

const Subtitle = styled.p`
  font-style: italic;
  margin-bottom: 20px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
  animation: ${slideIn} 0.5s ease-in-out;
`;

const Label = styled.label`
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
`;

const AnimatedButton = styled.button`
  background-color: ${(props) => props.theme.buttonBackground};
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  animation: ${pulse} 2s infinite;

  &:hover {
    background-color: ${(props) => props.theme.buttonHover};
    transform: scale(1.05);
  }

  &:disabled {
    background-color: #aaa;
    cursor: not-allowed;
    animation: none;
  }
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: ${(props) => props.theme.text};
  margin-top: 15px;
  transition: transform 0.3s;

  &:hover {
    transform: rotate(30deg);
  }
`;

const InfoToggle = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: ${(props) => props.theme.text};
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;

  &:hover {
    text-decoration: underline;
  }
`;

const InfoSection = styled.div`
  background: ${(props) => props.theme.infoBackground};
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  max-width: 600px;
  animation: ${fadeIn} 0.5s ease-in;
`;

const FeatureList = styled.ul`
  list-style-type: none;
  padding: 0;
`;

const FeatureItem = styled.li`
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;

  &:before {
    content: '✓';
    color: #28a745;
    font-weight: bold;
  }
`;

const Footer = styled.footer`
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: ${(props) => props.theme.text};
`;

export default LoginPage;
