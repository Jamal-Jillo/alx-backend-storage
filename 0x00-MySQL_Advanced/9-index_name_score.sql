-- Name: idx_name_first_score; Type: INDEX; Schema: alx; Owner: alx
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
