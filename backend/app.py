from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Voter(BaseModel):
    voter_id: str
    eligible: bool

class Candidate(BaseModel):
    candidate_id: str
    name: str
    vote_count: int = 0

class Vote(BaseModel):
    transaction_id: str
    candidate_id: str
    timestamp: str

voters = []
candidates = []
votes = []

@app.post('/register_voter/', response_model=Voter)
async def register_voter(voter: Voter):
    voters.append(voter)
    return voter

@app.post('/add_candidate/', response_model=Candidate)
async def add_candidate(candidate: Candidate):
    candidates.append(candidate)
    return candidate

@app.post('/cast_vote/', response_model=Vote)
async def cast_vote(vote: Vote):
    if not any(voter.voter_id == vote.transaction_id for voter in voters):
        raise HTTPException(status_code=400, detail="Voter not registered")
    candidate = next((c for c in candidates if c.candidate_id == vote.candidate_id), None)
    if candidate:
        candidate.vote_count += 1
        votes.append(vote)
        return vote
    raise HTTPException(status_code=404, detail="Candidate not found")

@app.get('/results/', response_model=List[Candidate])
async def get_results():
    return candidates
