import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async () => {
  try {
    const cronSecret = Deno.env.get("CRON_SECRET")
    
    if (!cronSecret) {
      return new Response(
        JSON.stringify({ error: "CRON_SECRET not configured" }), 
        { status: 500 }
      )
    }

    const response = await fetch("https://your-app.up.railway.app/run-ingestion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-cron-secret": cronSecret  
      }
    })

    const text = await response.text()
    
    return new Response(
      JSON.stringify({ 
        success: true, 
        message: text,
        status: response.status 
      }), 
      { 
        headers: { "Content-Type": "application/json" },
        status: 200 
      }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: error.message 
      }), 
      { 
        headers: { "Content-Type": "application/json" },
        status: 500 
      }
    )
  }
})