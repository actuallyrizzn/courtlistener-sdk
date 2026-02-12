"""
Example: Async/Concurrent Usage

This example demonstrates how to use the AsyncCourtListenerClient
to make concurrent API requests using async/await.
"""

import asyncio
from courtlistener import AsyncCourtListenerClient


async def single_request_example():
    """Example 1: Single async request"""
    print("1. Single Async Request:")
    
    async with AsyncCourtListenerClient() as client:
        courts = await client.courts.list(page=1)
        print(f"   Retrieved {len(courts.get('results', []))} courts")
    
    print()


async def concurrent_requests_example():
    """Example 2: Multiple concurrent requests"""
    print("2. Concurrent Requests:")
    
    async with AsyncCourtListenerClient() as client:
        # Run multiple requests concurrently
        results = await asyncio.gather(
            client.courts.list(page=1),
            client.dockets.list(page=1),
            client.opinions.list(page=1),
        )
        
        courts, dockets, opinions = results
        print(f"   Courts: {len(courts.get('results', []))} items")
        print(f"   Dockets: {len(dockets.get('results', []))} items")
        print(f"   Opinions: {len(opinions.get('results', []))} items")
    
    print()


async def error_handling_example():
    """Example 3: Error handling with async"""
    print("3. Error Handling:")
    
    async with AsyncCourtListenerClient() as client:
        try:
            # This will likely fail with a 404
            result = await client.get('nonexistent-endpoint/')
            print("   Success")
        except Exception as e:
            print(f"   Caught error: {type(e).__name__}: {str(e)}")
    
    print()


async def sequential_dependent_requests():
    """Example 4: Sequential requests where one depends on another"""
    print("4. Sequential Dependent Requests:")
    
    async with AsyncCourtListenerClient() as client:
        # First request
        courts = await client.courts.list(page=1)
        print(f"   First request: Retrieved {len(courts.get('results', []))} courts")
        
        # Use data from first request in second request
        if courts.get('results'):
            first_court = courts['results'][0]
            print(f"   Processing first court: {first_court.get('short_name', 'Unknown')}")
            
            # Make another request based on the first
            # (In real usage, you might use court ID to fetch related data)
            opinions = await client.opinions.list(page=1)
            print(f"   Second request: Retrieved {len(opinions.get('results', []))} opinions")
    
    print()


async def batch_with_limit():
    """Example 5: Concurrent requests with rate limiting"""
    print("5. Concurrent Requests with Limit:")
    
    async with AsyncCourtListenerClient() as client:
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent requests
        
        async def limited_request(endpoint, page):
            async with semaphore:
                result = await client.get(endpoint, params={'page': page})
                return len(result.get('results', []))
        
        # Make multiple requests with concurrency limit
        tasks = [
            limited_request('courts/', 1),
            limited_request('dockets/', 1),
            limited_request('opinions/', 1),
            limited_request('clusters/', 1),
        ]
        
        results = await asyncio.gather(*tasks)
        for i, count in enumerate(results):
            print(f"   Request {i+1}: {count} items")
    
    print()


async def main():
    """Run all examples"""
    print("=== Async CourtListener Client Examples ===\n")
    
    try:
        await single_request_example()
        await concurrent_requests_example()
        await error_handling_example()
        await sequential_dependent_requests()
        await batch_with_limit()
        
        print("=== Examples Complete ===")
    
    except Exception as e:
        print(f"\nFatal error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Run the async main function
    asyncio.run(main())
