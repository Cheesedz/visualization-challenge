"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
// import { Badge } from "@/components/ui/badge";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Camera,
  FileImage,
  Globe,
  UserPlus,
  Calculator,
  Paperclip,
  Send,
  ChevronRight,
} from "lucide-react";
import { IconFile, IconPaperclip, IconX } from "@tabler/icons-react";
import axios from "axios";

export default function HomePage() {
  const [inputValue, setInputValue] = useState("");
  const [selectedFile, setSelectedFile] = useState<File[] | null>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const fileArray = Array.from(files);
      setSelectedFile(fileArray);
    } else {
      setSelectedFile(null);
    }
    e.target.value = ""; // Reset the input value to allow re-uploading the same file
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Building:", inputValue);
    if (selectedFile) {
      console.log("With file:", selectedFile);
      // Add logic here to send the file and inputValue to your backend
      const rs = await axios.post(
        "http://localhost:8000/api/chat",
        {
          content: inputValue,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Response:", rs.data);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="flex items-center justify-between p-6 bg-white border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <img
            src="/logo.jpg"
            alt="Visual Suite Logo"
            className="h-10 w-auto"
          />
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">
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
                {selectedFile && selectedFile.length > 0 && (
                  <div className="flex flex-row space-x-2">
                    {selectedFile.map((file) => (
                      <div className="flex items-center justify-between bg-white border border-gray-200 rounded-lg px-3 shadow-sm">
                        <span className="flex items-center text-sm text-gray-800 truncate">
                          <IconPaperclip className="w-4 h-4 mr-2" /> {file.name}
                        </span>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => {
                            setSelectedFile((prev) =>
                              prev
                                ? prev.filter((f) => f.name !== file.name)
                                : []
                            );
                          }}
                          className="text-gray-500 hover:text-red-500 transition"
                          aria-label="Remove file"
                        >
                          <IconX className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
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
      </main>
    </div>
  );
}
