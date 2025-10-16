'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { WebsiteAnalyzer } from '../components/WebsiteAnalyzer';
import { ChatInterface } from '../components/ChatInterface';
import { ApiClient } from '../lib/api';
import { Brain, Globe, MessageSquare, Key, CheckCircle, AlertCircle } from 'lucide-react';

export default function HomePage() {
  const [apiKey, setApiKey] = useState('');
  const [isValidKey, setIsValidKey] = useState<boolean | null>(null);
  const [analyzedUrl, setAnalyzedUrl] = useState<string>('');
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    // Load API key from localStorage
    const savedKey = localStorage.getItem('apiKey');
    if (savedKey) {
      setApiKey(savedKey);
      // If we have a saved key, validate it immediately
      handleApiKeyChange(savedKey);
    }
  }, []);

  const handleApiKeyChange = async (key: string) => {
    setApiKey(key);
    localStorage.setItem('apiKey', key);

    if (key.trim()) {
      try {
        const apiClient = new ApiClient(key);
        await apiClient.healthCheck();
        setIsValidKey(true);
      } catch {
        setIsValidKey(false);
      }
    } else {
      setIsValidKey(null);
    }
  };

  const handleAnalysisComplete = (url: string) => {
    setAnalyzedUrl(url);
    setShowChat(true);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center">
            <Brain className="h-6 w-6 text-primary-foreground" />
          </div>
          <h1 className="text-4xl font-bold">Website Intelligence Agent</h1>
        </div>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          AI-powered agent for extracting, synthesizing, and interpreting key business insights from website homepages
        </p>
      </div>

      {/* API Key Setup */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            API Configuration
          </CardTitle>
          <CardDescription>
            Enter your API secret key to start analyzing websites
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              type="password"
              placeholder="Enter your API secret key"
              value={apiKey}
              onChange={(e) => handleApiKeyChange(e.target.value)}
              className="flex-1"
            />
            {isValidKey === true && (
              <div className="flex items-center gap-2 text-green-600">
                <CheckCircle className="h-5 w-5" />
                <span className="text-sm">Connected</span>
              </div>
            )}
            {isValidKey === false && (
              <div className="flex items-center gap-2 text-red-600">
                <AlertCircle className="h-5 w-5" />
                <span className="text-sm">Invalid key</span>
              </div>
            )}
          </div>
          <p className="text-sm text-muted-foreground">
            Your API key is stored locally in your browser and never sent to our servers.
          </p>
        </CardContent>
      </Card>

      {/* Main Content */}
      {(isValidKey || (apiKey && apiKey.trim().length > 0)) ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8" style={{ gridTemplateRows: '1fr' }}>
          {/* Website Analysis */}
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-2 mb-4">
              <Globe className="h-5 w-5" />
              <h2 className="text-2xl font-semibold">Website Analysis</h2>
              {isValidKey === null && apiKey && (
                <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                  Validating API key...
                </span>
              )}
            </div>
            <div className="flex-1">
              <WebsiteAnalyzer 
                apiKey={apiKey} 
                onAnalysisComplete={handleAnalysisComplete}
              />
            </div>
          </div>

          {/* Chat Interface */}
          {showChat && analyzedUrl && (
            <div className="flex flex-col h-full">
              <div className="flex items-center gap-2 mb-4">
                <MessageSquare className="h-5 w-5" />
                <h2 className="text-2xl font-semibold">AI Chat</h2>
              </div>
              <div className="flex-1">
                <ChatInterface apiKey={apiKey} analyzedUrl={analyzedUrl} />
              </div>
            </div>
          )}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <div className="space-y-4">
              <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto">
                <Key className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="text-xl font-semibold">API Key Required</h3>
              <p className="text-muted-foreground max-w-md mx-auto">
                Please enter a valid API secret key above to start analyzing websites and chatting with our AI.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Features */}
      <div className="mt-16">
        <h2 className="text-2xl font-semibold text-center mb-8">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mb-2">
                <Globe className="h-5 w-5 text-blue-600" />
              </div>
              <CardTitle className="text-lg">Smart Web Scraping</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Uses Jina AI Reader to extract clean, structured content from any website homepage.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center mb-2">
                <Brain className="h-5 w-5 text-green-600" />
              </div>
              <CardTitle className="text-lg">AI-Powered Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Powered by Google Gemini 2.5 Flash for intelligent business insight extraction.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center mb-2">
                <MessageSquare className="h-5 w-5 text-purple-600" />
              </div>
              <CardTitle className="text-lg">Conversational AI</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Ask follow-up questions and have natural conversations about analyzed websites.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
