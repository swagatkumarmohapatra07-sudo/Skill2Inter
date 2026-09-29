import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './store/AuthContext';
import Layout from './components/layout/Layout';

// Pages
import LoginPage from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProfilePage from './pages/Profile';
import ResumeAnalyzerPage from './pages/ResumeAnalyzer';
import InternshipsPage from './pages/Internships';
import MatchResultPage from './pages/MatchResult';
import RecommendationsPage from './pages/Recommendations';
import SkillGapPage from './pages/SkillGap';
import WhatIfPage from './pages/WhatIf';
import ComparePage from './pages/Compare';

// Route Guard
const ProtectedRoute = ({ children }) => {
  const { student, loading } = useAuth();
  if (loading) return null;
  if (!student) return <Navigate to="/login" replace />;
  return children;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="resume" element={<ResumeAnalyzerPage />} />
            
            <Route path="internships" element={<InternshipsPage />} />
            <Route path="match/:id" element={<MatchResultPage />} />
            
            <Route path="recommendations" element={<RecommendationsPage />} />
            <Route path="compare" element={<ComparePage />} />
            
            <Route path="skill-gap" element={<SkillGapPage />} />
            <Route path="what-if" element={<WhatIfPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
