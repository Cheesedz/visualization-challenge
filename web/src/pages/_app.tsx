import { AppProps } from "next/app";
import "@/styles/globals.css";
import Head from "next/head";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";

function MyApp({ Component, ...rest }: AppProps) {
  const [queryClient] = useState(() => new QueryClient());
  const router = useRouter();

  useEffect(() => {
    if (!router.pathname.includes("dashboard")) {
      document.body.style.backgroundColor = "var(--background)";
    } else {
      document.body.style.backgroundColor = "";
    }
  }, [router.pathname]);
  return (
    <>
      <Head>
        <title>Visual Suite</title>
        <link rel="icon" href="/logo.jpg" />
      </Head>
      <div className="w-full mx-auto">
        <QueryClientProvider client={queryClient}>
          <Component {...rest} />
        </QueryClientProvider>
      </div>
    </>
  );
}

export default MyApp;
