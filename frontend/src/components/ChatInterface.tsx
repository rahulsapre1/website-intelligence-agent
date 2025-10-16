'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { ChatResponse, ConversationMessage } from '@/types';
import { Send, Loader2, Bot, User } from 'lucide-react';

interface ChatInterfaceProps {
  apiKey: string;
  analyzedUrl: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function chatAboutWebsite(
  apiKey: string,
  url: string,
  query: string,
  conversationHistory?: Array<{ query: string; response: string }>
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url,
      query,
      conversation_history: conversationHistory,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      error: 'Network error',
      detail: `HTTP ${response.status}: ${response.statusText}`,
    }));
    throw new Error(error.detail || error.error);
  }

  return response.json();
}

export function ChatInterface({ apiKey, analyzedUrl }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ConversationMessage = {
      id: Date.now().toString(),
      query: input.trim(),
      response: '',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const conversationHistory = messages.map(msg => ({
        query: msg.query,
        response: msg.response,
      }));

      const response: ChatResponse = await chatAboutWebsite(
        apiKey,
        analyzedUrl,
        userMessage.query,
        conversationHistory
      );

      const botMessage: ConversationMessage = {
        id: (Date.now() + 1).toString(),
        query: userMessage.query,
        response: response.response,
        timestamp: response.timestamp,
      };

      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id ? botMessage : msg
      ));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      // Remove the user message if there was an error
      setMessages(prev => prev.filter(msg => msg.id !== userMessage.id));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const exampleQuestions = [
    "What is their pricing model?",
    "Who are their main competitors?",
    "What makes them unique?",
    "What is their target market?",
    "How do they make money?",
  ];

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="flex-shrink-0">
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-5 w-5" />
          Chat About Website
        </CardTitle>
        <CardDescription>
          Ask questions about {analyzedUrl}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-6 pt-0">
        {/* Messages */}
        <div className="flex-1 space-y-4 overflow-y-auto min-h-0">
          {messages.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground mb-4">
                Start a conversation about this website!
              </p>
              <div className="space-y-2">
                <p className="text-sm font-medium">Example questions:</p>
                <div className="flex flex-wrap gap-2 justify-center">
                  {exampleQuestions.map((question, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      onClick={() => setInput(question)}
                      className="text-xs"
                    >
                      {question}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="space-y-2">
                {/* User Message */}
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                      <User className="h-4 w-4 text-primary-foreground" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="bg-muted rounded-lg px-3 py-2">
                      <p className="text-sm">{message.query}</p>
                    </div>
                  </div>
                </div>

                {/* Bot Response */}
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                      <Bot className="h-4 w-4 text-secondary-foreground" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="bg-background border rounded-lg px-3 py-2">
                      {message.response ? (
                        <p className="text-sm whitespace-pre-wrap">{message.response}</p>
                      ) : loading ? (
                        <div className="flex items-center gap-2">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="text-sm text-muted-foreground">Thinking...</span>
                        </div>
                      ) : (
                        <p className="text-sm text-muted-foreground">Waiting for response...</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {/* Input - Fixed at bottom */}
        <div className="flex-shrink-0 pt-4 border-t">
          <div className="flex gap-2">
            <Input
              placeholder="Ask a question about this website..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <Button onClick={handleSendMessage} disabled={loading || !input.trim()}>
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
