export interface job {
  uuid: string;
  prompt: string;
  status: string;
}

const jobListEmpty: job[] = [];

export const useJobQueue = defineStore("useJobQueue", {
  state: () => ({
    joblist: useLocalStorage("joblist", jobListEmpty),
  }),
  actions: {
    set(joblist: job[]) {
      this.joblist = joblist;
    },
    // remove specific job
    remove(job: job) {
      this.joblist.forEach((item, index) => {
        if (item.uuid === job.uuid) this.joblist.splice(index, 1);
      });
    },
    add(job: job) {
      this.joblist.push(job);
    },
    update(job: job) {
      // try to find if job exist, if so update, otherwise add to the list
      const idx = this.joblist.findIndex((j) => j.uuid == job.uuid);
      if (idx >= 0) {
        this.joblist[idx] = job;
      } else {
        this.joblist.push(job);
      }
    },
  },
});
