'use client';

import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { ApiClient } from '../lib/api';
import { AnalyzeResponse, BusinessInsights } from '../types';
import { Loader2, Search, Copy, Check } from 'lucide-react';

interface WebsiteAnalyzerProps {
  apiKey: string;
  onAnalysisComplete?: (url: string) => void;
}

export function WebsiteAnalyzer({ apiKey, onAnalysisComplete }: WebsiteAnalyzerProps) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const apiClient = new ApiClient(apiKey);

  const handleAnalyze = async () => {
    if (!url.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiClient.analyzeWebsite(url.trim());
      setResult(response);
      if (onAnalysisComplete) {
        onAnalysisComplete(response.url);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const InsightCard = ({ title, value, icon }: { title: string; value: string; icon: React.ReactNode }) => (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center gap-2">
          {icon}
          <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm">{value || 'Not specified'}</p>
      </CardContent>
    </Card>
  );

  return (
    <div className="flex flex-col h-full space-y-6">
      {/* URL Input Section */}
      <Card className="flex-shrink-0">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Analyze Website
          </CardTitle>
          <CardDescription>
            Enter a website URL to extract business insights using AI
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
              disabled={loading}
            />
            <Button onClick={handleAnalyze} disabled={loading || !url.trim()}>
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4 mr-2" />
                  Analyze
                </>
              )}
            </Button>
          </div>
          
          {error && (
            <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <Card className="flex-1 flex flex-col">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Analysis Results</CardTitle>
                <CardDescription>
                  Business insights for {result.url}
                </CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => copyToClipboard(JSON.stringify(result, null, 2))}
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4 mr-2" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4 mr-2" />
                    Copy JSON
                  </>
                )}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <InsightCard
                title="Industry"
                value={result.insights.industry || ''}
                icon={<span className="text-blue-500">🏢</span>}
              />
              <InsightCard
                title="Company Size"
                value={result.insights.company_size || ''}
                icon={<span className="text-green-500">👥</span>}
              />
              <InsightCard
                title="Location"
                value={result.insights.location || ''}
                icon={<span className="text-orange-500">📍</span>}
              />
              <InsightCard
                title="Unique Value Proposition"
                value={result.insights.usp || ''}
                icon={<span className="text-purple-500">⭐</span>}
              />
              <InsightCard
                title="Products & Services"
                value={result.insights.products_services || ''}
                icon={<span className="text-red-500">🛍️</span>}
              />
              <InsightCard
                title="Target Audience"
                value={result.insights.target_audience || ''}
                icon={<span className="text-indigo-500">🎯</span>}
              />
            </div>

            {/* Contact Information */}
            {result.insights.contact_info && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-cyan-500">📞</span>
                    Contact Information
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {result.insights.contact_info.emails && result.insights.contact_info.emails.length > 0 && (
                      <div>
                        <h4 className="font-medium text-sm mb-2">Emails</h4>
                        <div className="space-y-1">
                          {result.insights.contact_info.emails.map((email, index) => (
                            <p key={index} className="text-sm text-muted-foreground">{email}</p>
                          ))}
                        </div>
                      </div>
                    )}
                    {result.insights.contact_info.phones && result.insights.contact_info.phones.length > 0 && (
                      <div>
                        <h4 className="font-medium text-sm mb-2">Phone Numbers</h4>
                        <div className="space-y-1">
                          {result.insights.contact_info.phones.map((phone, index) => (
                            <p key={index} className="text-sm text-muted-foreground">{phone}</p>
                          ))}
                        </div>
                      </div>
                    )}
                    {result.insights.contact_info.social_media && result.insights.contact_info.social_media.length > 0 && (
                      <div>
                        <h4 className="font-medium text-sm mb-2">Social Media</h4>
                        <div className="space-y-1">
                          {result.insights.contact_info.social_media.map((social, index) => (
                            <a key={index} href={social} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-500 hover:underline">
                              {social}
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
