from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent
from .database import SupabaseClient
import asyncio

class BookingWorkflow(Workflow):
    def __init__(self):
        super().__init__()
        self.db = SupabaseClient()

    @step
    async def search_tickets(self, event: StartEvent) -> StopEvent:
        try:
            showtimes = await self.db.get_showtimes()
            return StopEvent(result=showtimes)
        except Exception as e:
            return StopEvent(error=str(e))

    @step
    async def select_seats(self, event: StartEvent, showtime_id: str) -> StopEvent:
        try:
            showtime = await self.db.get_showtimes(showtime_id)
            return StopEvent(result=showtime)
        except Exception as e:
            return StopEvent(error=str(e))

    @step
    async def process_payment(self, event: StartEvent, booking_data: dict) -> StopEvent:
        try:
            booking = await self.db.create_booking(booking_data)
            return StopEvent(result=booking)
        except Exception as e:
            return StopEvent(error=str(e))

async def main():
    workflow = BookingWorkflow()
    result = await workflow.run()
    print(result)

# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
