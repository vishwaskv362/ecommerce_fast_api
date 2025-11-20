"""Pagination utilities."""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query
from ..config import settings

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = 1
    page_size: int = settings.DEFAULT_PAGE_SIZE
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 20
            }
        }
    
    def get_offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get the limit, ensuring it doesn't exceed max."""
        return min(self.page_size, settings.MAX_PAGE_SIZE)


class PageResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5,
                "has_next": True,
                "has_previous": False
            }
        }


def paginate(query: Query, params: PaginationParams) -> PageResponse:
    """Paginate a SQLAlchemy query."""
    total = query.count()
    
    items = query.offset(params.get_offset()).limit(params.get_limit()).all()
    
    total_pages = (total + params.page_size - 1) // params.page_size
    
    return PageResponse(
        items=items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        has_next=params.page < total_pages,
        has_previous=params.page > 1
    )
