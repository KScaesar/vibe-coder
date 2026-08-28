CREATE TABLE ad_request (
  id           BIGSERIAL PRIMARY KEY,
  placement_id TEXT NOT NULL,
  user_id      TEXT NOT NULL,
  created_at   TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE conversion_event (
  id            BIGSERIAL PRIMARY KEY,
  click_id      TEXT NOT NULL,
  conversion_id TEXT NOT NULL,
  amount        NUMERIC(12,2) NOT NULL,
  settled_at    TIMESTAMP
);
