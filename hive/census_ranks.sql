
DROP TABLE CENSUS_RANKS;
CREATE TABLE CENSUS_RANKS(
        COUNTY STRING,
        STATE STRING,
		JOBS_RETAIL float,
		JOBS_IT float,
		JOBS_RESEARCH float,
		JOBS_PUBLIC float,
		JOBS_EDUCATION float,
		HOUSING_COST_OWN float,
		HOUSING_COST_RENT float,
		POP_TOT float,
		POP_YOUNG float,
		pct_young float,
		jobs_retail_per_young float,
		jobs_retail_per_young_rank_st int,
		jobs_retail_per_young_rank_us int,
		jobs_it_per_young float,
		jobs_it_per_young_rank_st int,
		jobs_it_per_young_rank_us int,
		jobs_research_per_young float,
		jobs_research_per_young_rank_st int,
		jobs_research_per_young_rank_us int,
		jobs_public_per_young float,
		jobs_public_per_young_rank_st int,
		jobs_public_per_young_rank_us int,
		jobs_education_per_young float,
		jobs_education_per_young_rank_st int,
		jobs_education_per_young_rank_us int,
		housing_cost_own_rank_st int,
		housing_cost_own_rank_us int,
		housing_cost_rent_rank_st int,
		housing_cost_rent_rank_us int
)
COMMENT 'CENSUS Data With Ranks'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS ORC;

INSERT OVERWRITE TABLE CENSUS_RANKS
SELECT
	COUNTY,
	STATE,
	jobs_retail,
	jobs_it,
	jobs_research,
	jobs_public,
	jobs_education,
	housing_cost_own,
	housing_cost_rent,
	pop_tot,
	pop_young,
	pop_young/pop_tot as pct_young,
	
	JOBS_RETAIL/POP_YOUNG as JOBS_RETAIL_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_RETAIL/POP_YOUNG DESC) as JOBS_RETAIL_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_RETAIL/POP_YOUNG DESC) as JOBS_RETAIL_per_young_rank_us,
	
	JOBS_IT/POP_YOUNG as jobs_it_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_IT/POP_YOUNG DESC) as jobs_it_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_IT/POP_YOUNG DESC) as jobs_it_per_young_rank_us,
	
	JOBS_RESEARCH/POP_YOUNG as jobs_research_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_research/POP_YOUNG DESC) as jobs_research_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_research/POP_YOUNG DESC) as jobs_research_per_young_rank_us,

	JOBS_PUBLIC/POP_YOUNG as JOBS_PUBLIC_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_PUBLIC/POP_YOUNG DESC) as JOBS_PUBLIC_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_PUBLIC/POP_YOUNG DESC) as JOBS_PUBLIC_per_young_rank_us,
	
	JOBS_EDUCATION/POP_YOUNG as JOBS_EDUCATION_per_young,
	RANK() OVER(PARTITION BY STATE ORDER BY JOBS_EDUCATION/POP_YOUNG DESC) as JOBS_EDUCATION_per_young_rank_st,
	RANK() OVER(ORDER BY JOBS_EDUCATION/POP_YOUNG DESC) as JOBS_EDUCATION_per_young_rank_us,
				
	RANK() OVER(PARTITION BY STATE ORDER BY HOUSING_COST_OWN DESC) as housing_cost_own_rank_st,
	RANK() OVER(ORDER BY HOUSING_COST_OWN DESC) as housing_cost_own_rank_us,
	
	RANK() OVER(PARTITION BY STATE ORDER BY HOUSING_COST_RENT DESC) as housing_cost_rent_rank_st,
	RANK() OVER(ORDER BY HOUSING_COST_RENT DESC) as housing_cost_rent_rank_us
FROM CENSUS;