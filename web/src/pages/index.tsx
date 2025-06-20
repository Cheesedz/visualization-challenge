"use client";

import type React from "react";
import { useCallback, useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Globe, Paperclip, Send, Loader2 } from "lucide-react";
import { IconPaperclip, IconX } from "@tabler/icons-react";
import axios from "axios";

// Mock backend logs for demonstration
const mockLogs = [
  "🚀 Initializing Visual Suite AI...",
  "📁 Processing uploaded file...",
  "🔍 Analyzing file structure...",
  "⚡ Parsing YAML configuration...",
  "🧠 AI model loading...",
  "🔧 Setting up environment...",
  "📊 Generating visual components...",
  "🎨 Applying styling rules...",
  "🔗 Establishing connections...",
  "✅ Validation complete...",
  "🚀 Deploying to preview...",
  "🎉 Ready for preview!",
];

export default function HomePage() {
  const [inputValue, setInputValue] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [currentLogs, setCurrentLogs] = useState<string[]>([]);
  const [iframeLoading, setIframeLoading] = useState(true);
  const [iframeUrl, setIframeUrl] = useState("");
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isProcessing) return;

    const eventSource = new EventSource("http://localhost:8000/api/logs");

    // Correctly handle "log" event
    eventSource.addEventListener("log", (event) => {
      const log = event.data;
      console.log("Received log:", log);
      setCurrentLogs((prev) => [...prev, log]);
    });

    // Optional: handle ping/keep-alive if needed
    eventSource.addEventListener("ping", (event) => {
      // Optional: handle ping if you want to track activity
      // console.log("Ping received:", event.data);
    });

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [isProcessing]);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [currentLogs]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      setSelectedFile(files[0]);
    } else {
      setSelectedFile(null);
    }
    e.target.value = "";
  };

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (selectedFile || inputValue.trim()) {
        setIsProcessing(true);
        setCurrentLogs([]);
        setIframeLoading(true);
        setIframeUrl("");

        // Simulate API call
        try {
          const rs = await axios.post(
            "http://localhost:8000/api/chat",
            {
              content: inputValue,
              file: selectedFile,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Response:", rs.data.url);
          setIsProcessing(false);
          setIsFinished(true);
          setIframeUrl(rs.data.url); // Replace with your actual URL
        } catch (error) {
          console.error("Error:", error);
        }
      }
    },
    [selectedFile, inputValue]
  );

  const resetToInitialState = () => {
    setIsProcessing(false);
    setCurrentLogs([]);
    setIframeLoading(true);
    setIframeUrl("");
    setInputValue("");
    setSelectedFile(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <div
            className="w-10 h-10 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-lg flex items-center justify-center cursor-pointer"
            onClick={resetToInitialState}
          >
            <span className="text-white font-bold text-lg">VS</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main
        className={`transition-all duration-700 ease-in-out ${
          isProcessing ? "max-w-7xl" : "max-w-4xl"
        } mx-auto px-6 py-12`}
      >
        {!isProcessing && !isFinished ? (
          // Initial Single Column Layout
          <div className="animate-in fade-in duration-500">
            {/* Beta Badge */}
            <div className="flex justify-center mb-8">
              <Badge className="p-2 text-sm bg-gradient-to-r from-emerald-400 to-cyan-400 text-black hover:from-emerald-500 hover:to-cyan-500">
                🚀 The Visual AI Playground is now launch.
              </Badge>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-4xl font-bold text-center text-gray-900 mb-12">
              What can I help you power with AI?
            </h1>

            {/* Input Section */}
            <form onSubmit={handleSubmit} className="mb-8">
              <div className="relative">
                <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                  <div className="flex items-start space-x-4 flex-col w-full">
                    {selectedFile && (
                      <div className="flex flex-row space-x-2">
                        <div className="flex items-center justify-between bg-white border border-gray-200 rounded-lg px-3 shadow-sm">
                          <span className="flex items-center text-sm text-gray-800 truncate">
                            <IconPaperclip className="w-4 h-4 mr-2" />{" "}
                            {selectedFile.name}
                          </span>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setSelectedFile(null)}
                            className="text-gray-500 hover:text-red-500 transition"
                            aria-label="Remove file"
                          >
                            <IconX className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    )}
                    <div className="flex flex-row w-full">
                      <div className="flex w-full items-center space-x-2">
                        <Input
                          value={inputValue}
                          onChange={(e) => setInputValue(e.target.value)}
                          placeholder="Ask Visual Suite to build..."
                          className="border-0 bg-transparent text-lg placeholder:text-gray-500 focus-visible:ring-0 focus-visible:ring-offset-0"
                        />
                      </div>
                      <div className="flex items-end space-x-2">
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="hover:bg-gray-100 relative"
                          asChild
                        >
                          <label>
                            <Input
                              type="file"
                              multiple
                              accept=".yaml,.yml"
                              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                              onChange={handleFileChange}
                            />
                            <Paperclip className="w-5 h-5" />
                          </label>
                        </Button>
                        <Button
                          type="submit"
                          variant="ghost"
                          size="icon"
                          className="hover:bg-gray-100 relative"
                        >
                          <Send className="w-5 h-5" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        ) : (
          // Two Column Processing Layout
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-8rem)] animate-in slide-in-from-bottom duration-700">
            {/* Left Column - Logs */}
            <div className="animate-in slide-in-from-left duration-500 delay-200">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    Thinking
                  </CardTitle>
                  <CardDescription>Real-time chain of thoughts</CardDescription>
                </CardHeader>
                <CardContent className="h-[calc(100%-5rem)] overflow-hidden">
                  <div className="bg-black rounded-lg p-4 max-h-124 overflow-y-auto font-mono text-sm border">
                    <div className="space-y-2">
                      {currentLogs.map((log, index) => (
                        <div
                          key={index}
                          className="text-green-400 animate-in slide-in-from-bottom duration-300"
                          style={{ animationDelay: `${index * 100}ms` }}
                        >
                          <span className="text-gray-500 mr-2">
                            [{new Date().toLocaleTimeString()}]
                          </span>
                          {log}
                        </div>
                      ))}
                      {currentLogs.length > 0 && (
                        <div className="flex items-center text-green-400">
                          <span className="text-gray-500 mr-2">
                            [{new Date().toLocaleTimeString()}]
                          </span>
                          <Loader2 className="w-4 h-4 animate-spin mr-2" />
                          Thinking...
                        </div>
                      )}
                      <div ref={logsEndRef} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Right Column - Preview */}
            <div className="animate-in slide-in-from-right duration-500 delay-400">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="w-5 h-5" />
                    Live Preview
                  </CardTitle>
                  <CardDescription>
                    Your AI-generated application preview
                  </CardDescription>
                </CardHeader>
                <CardContent className="h-[calc(100%-5rem)] p-0">
                  <div className="relative w-full h-full bg-gray-100 rounded-lg overflow-hidden">
                    {iframeLoading && (
                      <div className="absolute inset-0 flex items-center justify-center bg-white z-10">
                        <div className="text-center">
                          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-emerald-500" />
                          <p className="text-gray-600">Loading preview...</p>
                          <div className="mt-4 flex justify-center space-x-1">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                            <div
                              className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"
                              style={{ animationDelay: "0.1s" }}
                            ></div>
                            <div
                              className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"
                              style={{ animationDelay: "0.2s" }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    )}
                    {/* {iframeUrl && ( */}
                    <iframe
                      src={
                        "https://chgoenqlvkivddoqvuzm.supabase.co/storage/v1/object/public/visualization-challenge/public/text-classification.html"
                      }
                      className={`w-full h-full border-0 transition-opacity duration-500 ${
                        iframeLoading ? "opacity-0" : "opacity-100"
                      }`}
                      title="AI Generated Preview"
                      onLoad={() => setIframeLoading(false)}
                    />
                    {/* )} */}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
